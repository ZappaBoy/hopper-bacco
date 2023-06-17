import threading
from queue import Queue

import requests
from fastapi import Response

from routes.hopper.dto.hopper_model import HopperDto
from routes.services.ip_rotator_service import IpRotatorService
from routes.services.user_agent_rotator_service import UserAgentRotatorService
from shared.utilities.configurator import Configurator
from shared.utilities.logger import Logger


class HopperService:
    def __init__(self):
        self.logger = Logger(self.__class__.__name__)
        self.user_agent_rotator_service = UserAgentRotatorService.instance()
        self.ip_rotator_service = IpRotatorService.instance()
        self.timeout = Configurator.instance().get_request_timeout_seconds()
        self.proxy_countries = Configurator.instance().get_proxy_countries()
        self.thread_finished = threading.Event()

    def proxy(self, hopper_dto: HopperDto) -> Response:
        self.logger.debug(f"Proxying request: {hopper_dto}")
        session = requests.Session()

        headers = hopper_dto.headers if hopper_dto.headers is not None else session.headers
        headers['User-Agent'] = self.user_agent_rotator_service.get_random_user_agent()
        headers['Content-Type'] = hopper_dto.type
        proxies = self.ip_rotator_service.get_random_proxy_list(countries=self.proxy_countries)

        queue = Queue()
        self.thread_finished = threading.Event()
        args = (queue, session, hopper_dto, headers)
        threads = [threading.Thread(target=self.execute_queue_request, args=args + (proxies[i],))
                   for i in range(len(proxies))]
        for thread in threads:
            thread.daemon = True
            thread.start()

        self.thread_finished.wait()
        response = queue.get()
        if response.ok:
            return Response(content=response.content, media_type=hopper_dto.type,
                            status_code=response.status_code)
        else:
            raise Exception('Error proxying request: ' + str(response.status_code) + ' # ' + response.text)

    def execute_queue_request(self, queue: Queue, session: requests.Session, hopper_dto: HopperDto, headers: dict,
                              proxy: str) -> None:
        proxy_map = {"http": proxy, "https": proxy}
        try:
            response = session.request(method=hopper_dto.method, url=hopper_dto.url, params=hopper_dto.params,
                                       headers=headers, data=hopper_dto.data, proxies=proxy_map, json=hopper_dto.body,
                                       timeout=self.timeout)
            queue.put(response)
            self.thread_finished.set()
        except Exception as e:
            self.logger.debug(f"Error proxying request: {e}")

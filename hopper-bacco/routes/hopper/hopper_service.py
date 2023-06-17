import threading
from queue import Queue

import requests

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

    def proxy(self, hopper_dto: HopperDto) -> dict:
        self.logger.debug(f"Proxying request: {hopper_dto}")
        session = requests.Session()

        headers = hopper_dto.headers
        headers['User-Agent'] = self.user_agent_rotator_service.get_random_user_agent()
        proxies = self.ip_rotator_service.get_random_proxy_list(countries=self.proxy_countries)

        queue = Queue()
        args = (queue, session, hopper_dto, headers)
        threads = [threading.Thread(target=self.execute_queue_request, args=args + (proxies[i],))
                   for i in range(len(proxies))]
        for thread in threads:
            thread.daemon = True
            thread.start()

        response = queue.get()

        if response.ok:
            return response.json()
        else:
            raise Exception('Error proxying request: ' + str(response.status_code) + ' # ' + response.text)

    def execute_queue_request(self, queue: Queue, session: requests.Session, hopper_dto: HopperDto, headers: dict,
                              proxy: str) -> None:
        proxy_map = {"http": proxy, "https": proxy}
        response = session.request(method=hopper_dto.method, url=hopper_dto.url, params=hopper_dto.params,
                                   headers=headers, data=hopper_dto.body, proxies=proxy_map,
                                   timeout=self.timeout)
        queue.put(response)

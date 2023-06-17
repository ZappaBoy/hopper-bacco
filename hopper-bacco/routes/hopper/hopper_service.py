from typing import List

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
        headers['User-Agent'] = self.get_random_user_agent()

        proxies = self.ip_rotator_service.get_random_proxy_list(countries=self.proxy_countries)
        response = self.execute_request(session=session, hopper_dto=hopper_dto, headers=headers, proxies=proxies)

        if response.ok:
            return response.json()
        else:
            raise Exception('Error proxying request: ' + str(response.status_code) + ' # ' + response.text)

    def get_random_user_agent(self) -> str:
        return self.user_agent_rotator_service.get_random_user_agent()

    def execute_request(self, session: requests.Session, hopper_dto: HopperDto, headers: dict, proxies: List[str]) \
            -> requests.Response:
        for proxy in proxies:
            try:
                proxy_map = {
                    "http": proxy,
                    "https": proxy
                }
                response = session.request(method=hopper_dto.method, url=hopper_dto.url, params=hopper_dto.params,
                                           headers=headers, data=hopper_dto.body, proxies=proxy_map,
                                           timeout=self.timeout)
                return response
            except Exception as e:
                self.logger.error(f"Error proxying request: {e}")
                continue

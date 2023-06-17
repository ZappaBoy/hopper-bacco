from routes.hopper.dto.hopper_model import HopperDto
from routes.services.user_agent_service import UserAgentService
from shared.utilities.logger import Logger
from shared.utilities.utilities import get_requests_session

REQUESTS_TIMEOUT_SECONDS = 100


class HopperService:
    def __init__(self):
        self.logger = Logger(self.__class__.__name__)
        self.user_agent_service = UserAgentService.instance()

    def proxy(self, hopper_dto: HopperDto) -> dict:
        self.logger.debug(f"Proxying request: {hopper_dto}")
        session = get_requests_session()

        spoofed_headers = hopper_dto.headers
        spoofed_headers['User-Agent'] = self.get_random_user_agent()
        response = session.request(method=hopper_dto.method, url=hopper_dto.url, params=hopper_dto.params,
                                   headers=spoofed_headers, data=hopper_dto.body,
                                   timeout=REQUESTS_TIMEOUT_SECONDS)
        if response.ok:
            return response.json()
        else:
            raise Exception('Error proxying request: ' + str(response.status_code) + ' # ' + response.text)

    def get_random_user_agent(self) -> str:
        return self.user_agent_service.get_random_user_agent()

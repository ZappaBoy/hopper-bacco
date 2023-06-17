from routes.hopper.dto.hopper_model import HopperDto
from shared.utilities.logger import Logger
from shared.utilities.utilities import get_requests_session

REQUESTS_TIMEOUT_SECONDS = 100


class HopperService:
    def __init__(self):
        self.logger = Logger(self.__class__.__name__)

    def proxy(self, hopper_dto: HopperDto) -> dict:
        self.logger.debug(f"Proxying request: {hopper_dto}")
        session = get_requests_session()

        response = session.request(method=hopper_dto.method, url=hopper_dto.url, params=hopper_dto.params,
                                   headers=hopper_dto.headers, data=hopper_dto.body,
                                   timeout=REQUESTS_TIMEOUT_SECONDS)
        if response.ok:
            return response.json()
        else:
            raise Exception('Error proxying request: ' + str(response.status_code) + ' # ' + response.text)

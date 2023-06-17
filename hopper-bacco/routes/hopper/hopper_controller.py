from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from routes.hopper.hopper_service import HopperService
from shared.deps.api_key_auth import ApiKeyAuth
from shared.utilities.logger import Logger

router = InferringRouter()


@cbv(router)
class HopperController:
    api_key_auth = ApiKeyAuth()

    def __init__(self):
        self.logger = Logger(self.__class__.__name__)
        self.router = router
        self.hopper_service = HopperService()

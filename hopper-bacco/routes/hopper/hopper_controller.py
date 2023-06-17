from fastapi import Depends
from fastapi.openapi.models import APIKey
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from routes.hopper.dto.hopper_model import HopperDto
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

    # TODO: add real proxy logic
    @router.post("/")
    def proxy(self, hopper_dto: HopperDto, api_key: APIKey = Depends(api_key_auth.check_api_key)) -> dict:
        return self.hopper_service.proxy(hopper_dto)

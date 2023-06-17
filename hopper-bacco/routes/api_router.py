from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from routes.hopper.hopper_controller import HopperController
from shared.utilities.logger import Logger

router = InferringRouter()


@cbv(router)
class APIRouter:
    def __init__(self):
        self.logger = Logger(self.__class__.__name__)
        self.router = router
        hopper_controller = HopperController()

        self.include(hopper_controller, prefix="/hop")

    @staticmethod
    def include(external_router, **kwargs):
        router.include_router(external_router.router, **kwargs)

    @router.get("/health/check")
    def healthcheck(self):
        return {"Status": "Alive"}

import traceback

from starlette import status
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Scope, Receive, Send

from shared.models.status_message import StatusMessage
from shared.utilities.configurator import Configurator
from shared.utilities.logger import Logger


class ExceptionHandlerMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.logger = Logger(self.__class__.__name__)
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        try:
            await self.app(scope, receive, send)
        except Exception as exception:
            if Configurator.instance().is_debug():
                self.logger.debug(f'Exception occurred: {traceback.format_exc()}')
            else:
                self.logger.error(f'Exception occurred: {exception}')
            status_message = StatusMessage(detail='Something goes wrong')
            response = JSONResponse(content=status_message.dict(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            await response(scope, receive, send)

from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from starlette import status

from shared.utilities.configurator import Configurator
from shared.utilities.logger import Logger


class ApiKeyAuth:
    configurator = Configurator.instance()
    api_key_header = APIKeyHeader(name=configurator.get_api_key_header(), auto_error=False)

    def __init__(self):
        self.logger = Logger(self.__class__.__name__)

    def check_api_key(self, api_key: str = Security(api_key_header)):
        if api_key != self.configurator.get_api_key():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Forbidden"
            )

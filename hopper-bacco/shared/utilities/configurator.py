from typing import List

from shared.decorators.singleton import Singleton
from shared.models.settings.environment import Environment
from shared.models.settings.log_level import LogLevel
from shared.models.settings.settings import Settings


@Singleton
class Configurator:
    def __init__(self):
        self._settings = Settings()
        if self._settings.environment == Environment.testing:
            self._settings.log_level = LogLevel.debug

    def is_production_environment(self) -> bool:
        return self._settings.environment == Environment.production

    def is_debug(self) -> bool:
        return self._settings.log_level == LogLevel.debug

    def get_api_key_header(self) -> str:
        return self._settings.api_key_header

    def get_api_key(self) -> str:
        return self._settings.api_key

    def get_request_timeout_seconds(self) -> int:
        return self._settings.request_timeout_seconds

    def get_proxy_countries(self) -> List[str]:
        return self._settings.proxy_countries

    def get_settings(self) -> Settings:
        return self._settings

from typing import List

from fp.fp import FreeProxy

from shared.decorators.singleton import Singleton
from shared.utilities.logger import Logger


@Singleton
class IpRotatorService:
    def __init__(self):
        self.logger = Logger(self.__class__.__name__)

    @staticmethod
    def get_random_proxy_list(countries: List[str] = None) -> List[str]:
        if countries is None or len(countries) == 0:
            countries = ["IT", "FR", "DE", "ES", "GB"]
        return FreeProxy(country_id=countries, rand=True).get_proxy_list(repeat=True)

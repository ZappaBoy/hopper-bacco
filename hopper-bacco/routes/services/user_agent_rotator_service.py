from random_user_agent.params import SoftwareName, OperatingSystem, Popularity
from random_user_agent.user_agent import UserAgent

from shared.decorators.singleton import Singleton
from shared.utilities.logger import Logger


@Singleton
class UserAgentRotatorService:
    def __init__(self):
        self.logger = Logger(self.__class__.__name__)
        software_names = [SoftwareName.CHROME.value, SoftwareName.FIREFOX.value, SoftwareName.EDGE.value]
        operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value, OperatingSystem.MAC_OS_X.value]
        popularities = [Popularity.POPULAR.value, Popularity.COMMON.value]
        self.user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems,
                                            popularity=popularities)

    def get_random_user_agent(self) -> str:
        return self.user_agent_rotator.get_random_user_agent()

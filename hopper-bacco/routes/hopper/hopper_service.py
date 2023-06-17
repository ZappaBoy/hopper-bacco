from shared.utilities.logger import Logger


class HopperService:
    def __init__(self):
        self.logger = Logger(self.__class__.__name__)

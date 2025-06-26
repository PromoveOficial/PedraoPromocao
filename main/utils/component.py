import logging

class Component():
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.__init_logger()
    
    def __init_logger(self):
        if not self.logger.hasHandlers():
            self.logger.setLevel(logging.DEBUG)

            handler = logging.StreamHandler()

            formatter = logging.Formatter(
                # '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                '[%(asctime)s] [%(levelname)s] %(message)s'
            )

            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
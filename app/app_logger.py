import logging
import logging.config

class AppLogger:

    def __init__(self) -> None:
        logging.config.fileConfig(fname='logging.ini', disable_existing_loggers=False)
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

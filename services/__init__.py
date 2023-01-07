from logs.log_base import logging, f_handler, c_handler


class BaseController(object):

    def __init__(self):
        """ logging option """
        """ If you want to add log handler you have to add below snippet into the target base class init def """
        logger = logging.getLogger(self.__module__)
        logger.addHandler(f_handler)
        logger.addHandler(c_handler)
        self.logger = logger
        """ end """
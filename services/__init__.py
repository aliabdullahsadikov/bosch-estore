from logs.log_base import logging, file_error_handler, file_info_handler, console_handler


class BaseController(object):

    def __init__(self):
        # self.user = get_user()
        """ logging option """
        """ If you want to add log handler you have to add below snippet into the target base class init def """
        logger = logging.getLogger(self.__module__)
        logger.addHandler(file_error_handler)
        logger.addHandler(file_info_handler)
        logger.addHandler(console_handler)
        self.logger = logger
        """ end """
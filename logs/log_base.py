
""" with yaml file """
# import logging
# import logging.config
# import os
#
# import yaml
#
# from common.utils import get_root_dir
#
# with open('logs/log.yaml', 'r') as f:
#     config = yaml.safe_load(f.read())
#     logging.config.dictConfig(config)
#
# log_name = os.path.join(get_root_dir(), config['handlers']['error_file_handler']['filename'])
# config['handlers']['error_file_handler']['filename'] = log_name

# logger = logging.getLogger(__name__)
#
# logger.debug('This is a debug message')
import logging

""" yaml end """

""" with config file """
# import logging
# import logging.config
# import os.path
#
# full_path = os.path.abspath('logs/log_files/error.log')
# logging.config.fileConfig(fname='log.conf', defaults={'core': f"{full_path}logs/log_files/error.log"}, disable_existing_loggers=False)

""" config end """

""" other method """
# Create a custom logger
# logger = logging.getLogger(__name__)

# Create handlers
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)

# file error handler
file_error_handler = logging.FileHandler('logs/log_files/error.log')
file_error_handler.setLevel(logging.ERROR)

# file info handler
file_info_handler = logging.FileHandler('logs/log_files/info.log')
file_info_handler.setLevel(logging.INFO)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(c_format)

f_format = logging.Formatter("%(levelname)s <PID %(process)d:%(processName)s> %(name)s.%(funcName)s(): %(message)s")
file_error_handler.setFormatter(f_format)
file_info_handler.setFormatter(f_format)

# Add handlers to the logger
# logger.addHandler(c_handler)
# logger.addHandler(f_handler)

# logger.warning('This is a warning')
# logger.error('This is an error')
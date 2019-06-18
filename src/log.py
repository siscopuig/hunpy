import logging
import os
import datetime
from utils.utils_files import get_project_root_abs_path

class Log:

    # https://docs.python.org/3/library/logging.html
    # https://docs.python.org/3/howto/logging-cookbook.html

    # Formatter
    # '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    def __init__(self):

        # Get an instance from logging
        self.logger = logging.getLogger(__name__)

    def open_log(self, config, debug=False):

        string_format = config['log.string.format']
        date_format = config['log.date.format']
        log_dir = config['log.dir']
        log_name = config['log.name']

        date = datetime.datetime.now().strftime(date_format)
        abs_log_path = get_project_root_abs_path(log_dir)
        filename = '{log_dir}/{name}_{date}.log'.format(log_dir=log_dir, name=log_name, date=date)
        
        # Finds project root directory
        log_filepath = get_project_root_abs_path(filename)

        # Create file in log directory
        try:
            if not os.path.exists(abs_log_path):
                os.makedirs(abs_log_path)
        except OSError:
            print('Error: Creating directory. ' + abs_log_path)

        level = logging.DEBUG if debug else logging.INFO

        self.logger.setLevel(level)
        formatter = logging.Formatter(string_format)

        fh = logging.FileHandler(filename=log_filepath,
                                 mode='a',
                                 encoding=None,
                                 delay=False)
        fh.setLevel(level)
        fh.setFormatter(formatter)

        sh = logging.StreamHandler()
        sh.setLevel(level)
        sh.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(sh)

    def set_level(self, level):
        """
        Set the logging level of this logger.
        level must be an int or a str.

        (DEBUG, INFO, WARNING, ERROR, CRITICAL)

        """

        self.logger.setLevel(level)

    def debug(self, *args, **kwargs):

        logging.LoggerAdapter(self.logger, extra='').debug(*args, **kwargs)

    def info(self, *args, **kwargs):

        logging.LoggerAdapter(self.logger, extra='').info(*args, **kwargs)

    def warning(self, *args, **kwargs):

        logging.LoggerAdapter(self.logger, extra='').warning(*args, **kwargs)

    def error(self, *args, **kwargs):

        logging.LoggerAdapter(self.logger, extra='').error(*args, **kwargs)

    def critical(self, *args, **kwargs):

        logging.LoggerAdapter(self.logger, extra='').critical(*args, **kwargs)

    def exception(self, *args, **kwargs):

        logging.LoggerAdapter(self.logger, extra='').exception(*args, **kwargs)

    def close(self):

        self.info('Log End')

        handlers = self.logger.handlers
        for handler in handlers:
            handler.close()
            self.logger.removeHandler(handler)

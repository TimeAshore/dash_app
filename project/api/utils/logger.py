# services/socamas/project/api/utils/logger.py

"""
Setup a nice formatter, configurable level, and timedrotatingfile handler for logging.
"""

import logging
import platform
from logging.handlers import TimedRotatingFileHandler


class Logging(object):
    """Configure flask logging with nice formatting , timedrotatingfile support."""

    def __init__(self, app: object = None, log_dir: object = "") -> object:
        """Boiler plate extension init with log_level being declared"""
        self.log_level = None
        self.app = app
        self.dir = log_dir
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Setup the logging handlers, level and formatters.
        """
        config_log_level = app.config.get('LOG_LEVEL', None)

        # Set up format for default logging
        hostname = platform.node().split('.')[0]
        formatter = ("%(asctime)s | %(process)d [%(name)s] | "
                     "%(pathname)s:%(lineno)d | %(funcName)s | "
                     "%(levelname)s | [{hostname}] - %(message)s ").\
            format(hostname=hostname)

        config_log_int = None
        set_level = None

        if config_log_level:
            config_log_int = getattr(logging, config_log_level.upper(), None)
            if not isinstance(config_log_int, int):
                raise ValueError(
                    'Invalid log level: {0}'.format(config_log_level)
                )
            set_level = config_log_int

        # Set to NotSet if we still aren't set yet
        if not set_level:
            set_level = config_log_int = logging.NOTSET
        self.log_level = set_level

        # Setup basic StreamHandler logging with format and level
        logging.basicConfig(format=formatter)
        root_logger = logging.getLogger()

        # Get everything ready to setup the timedrotatingfile handler
        filename = "{}/socamas_server_web".format(self.dir)
        when = "D"  # 每天生成日志文件
        interval = 1  # 每天生成一个日志文件
        backup = 0  # 保留全部日志
        encoding = "utf-8"
        suffix = "%Y-%m-%d.log"
        trfHandler = TimedRotatingFileHandler(filename=filename,
                                              when=when,
                                              interval=interval,
                                              backupCount=backup,
                                              encoding=encoding)
        trfHandler.suffix = suffix
        trfHandler.setLevel(set_level)
        root_logger.addHandler(trfHandler)
        self.set_formatter(formatter)

        return config_log_int

    @staticmethod
    def set_formatter(log_formatter):
        """Override the default log formatter with your own."""
        # Add our formatter to all the handlers
        root_logger = logging.getLogger()
        for handler in root_logger.handlers:
            handler.setFormatter(logging.Formatter(log_formatter))

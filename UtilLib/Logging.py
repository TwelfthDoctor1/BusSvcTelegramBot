import enum
import datetime
from warnings import warn
from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger
from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger


class LoggingLevel(enum.IntEnum):
    """
    LoggingLevel is an enum class used to determine the logging level of the logging activity.
    Alternatively they can be used for other cases such as testing for specific levels, etc.

    Levels are sorted in terms of their priority.

    """
    DEBUG = -2
    LOG = -1
    NONE = 0
    INFO = 1
    WARN = 2
    ERROR = 3
    ASSERT_ERROR = 4
    EXCEPTION = 5


class LoggerClass(ApprenticeLogger):
    """
    A Logger referencing from the ApprenticeLogger.

    Modified to include logging to console.
    """
    def __init__(self, module_name=None, main_owner=None, additional_context=None):
        super(LoggerClass, self).__init__(
            module_name=module_name,
            main_owner=main_owner,
            additional_context=additional_context
        )
        self.mlog = MasterLogger(
            module_name=module_name,
            main_owner=main_owner,
            additional_context=additional_context
        )

    def info(self, message, owner=None, to_console=True, to_master=True, to_apprentice=False):
        if to_apprentice is True:
            super(LoggerClass, self).info(
                message=message,
                owner=owner
            )

        if to_master is True:
            self.mlog.info(
                message=message,
                owner=owner
            )

        if to_console is True:
            dt = datetime.datetime.now()
            print(f"[{dt.day} {dt.strftime('%B')} {dt.year} | {dt.strftime('%I')}:{dt.strftime('%M')}:{dt.strftime('%S')} {dt.strftime('%p')}"
                  f" | {self.module_name}] {message}")
            print("==============================================================================================================")

    def log(self, message, owner=None, to_console=True, to_master=False, to_apprentice=True):
        if to_apprentice is True:
            super(LoggerClass, self).log(
                message=message,
                owner=owner
            )

        if to_master is True:
            self.mlog.log(
                message=message,
                owner=owner
            )

        if to_console is True:
            dt = datetime.datetime.now()
            print(f"[{dt.day} {dt.strftime('%B')} {dt.year} | {dt.strftime('%I')}:{dt.strftime('%M')}:{dt.strftime('%S')} {dt.strftime('%p')}"
                  f" | {self.module_name}] {message}")
            print("==============================================================================================================")

    def debug(self, message, owner=None, to_console=True, to_master=False, to_apprentice=True):
        if to_apprentice is True:
            super(LoggerClass, self).debug(
                message=message,
                owner=owner
            )

        if to_master is True:
            self.mlog.debug(
                message=message,
                owner=owner
            )

        if to_console is True:
            dt = datetime.datetime.now()
            print(f"[{dt.day} {dt.strftime('%B')} {dt.year} | {dt.strftime('%I')}:{dt.strftime('%M')}:{dt.strftime('%S')} {dt.strftime('%p')}"
                  f" | {self.module_name}] {message}")
            print("==============================================================================================================")

    def warn(self, message, owner=None, to_console=True, to_master=False, to_apprentice=True):
        if to_apprentice is True:
            super(LoggerClass, self).warn(
                message=message,
                owner=owner
            )

        if to_master is True:
            self.mlog.warn(
                message=message,
                owner=owner
            )

        if to_console is True:
            dt = datetime.datetime.now()
            warn(f"[{dt.day} {dt.strftime('%B')} {dt.year} | {dt.strftime('%I')}:{dt.strftime('%M')}:{dt.strftime('%S')} {dt.strftime('%p')}"
                  f" | {self.module_name}] {message}")
            print("==============================================================================================================")

    def error(self, message, owner=None, to_console=True, to_master=False, to_apprentice=True):
        if to_apprentice is True:
            super(LoggerClass, self).error(
                message=message,
                owner=owner
            )

        if to_master is True:
            self.mlog.error(
                message=message,
                owner=owner
            )

        if to_console is True:
            dt = datetime.datetime.now()
            warn(f"[{dt.day} {dt.strftime('%B')} {dt.year} | {dt.strftime('%I')}:{dt.strftime('%M')}:{dt.strftime('%S')} {dt.strftime('%p')}"
                  f" | {self.module_name}] {message}")
            print("==============================================================================================================")

    def assert_error(self, message, owner=None, to_console=True, to_master=False, to_apprentice=True):
        if to_apprentice is True:
            super(LoggerClass, self).assert_error(
                message=message,
                owner=owner
            )

        if to_master is True:
            self.mlog.assert_error(
                message=message,
                owner=owner
            )

        if to_console is True:
            dt = datetime.datetime.now()
            warn(f"[{dt.day} {dt.strftime('%B')} {dt.year} | {dt.strftime('%I')}:{dt.strftime('%M')}:{dt.strftime('%S')} {dt.strftime('%p')}"
                  f" | {self.module_name}] {message}")
            print("==============================================================================================================")

    def exception(self, message, owner=None, to_console=True, to_master=False, to_apprentice=True):
        if to_apprentice is True:
            super(LoggerClass, self).exception(
                message=message,
                owner=owner
            )

        if to_master is True:
            self.mlog.exception(
                message=message,
                owner=owner
            )

        if to_console is True:
            dt = datetime.datetime.now()
            warn(f"[{dt.day} {dt.strftime('%B')} {dt.year} | {dt.strftime('%I')}:{dt.strftime('%M')}:{dt.strftime('%S')} {dt.strftime('%p')}"
                  f" | {self.module_name}] {message}")
            print("==============================================================================================================")

    def log_level(self, message, owner=None, to_console=True, to_master=False, to_apprentice=True, level: LoggingLevel = LoggingLevel.INFO):
        if level == LoggingLevel.DEBUG:
            self.debug(message, owner, to_console)
        elif level == LoggingLevel.LOG:
            self.log(message, owner, to_console)
        elif level == LoggingLevel.INFO:
            self.info(message, owner, to_console)
        elif level == LoggingLevel.WARN:
            self.warn(message, owner, to_console)
        elif level == LoggingLevel.ERROR:
            self.error(message, owner, to_console)
        elif level == LoggingLevel.ASSERT_ERROR:
            self.assert_error(message, owner, to_console)
        elif level == LoggingLevel.EXCEPTION:
            self.exception(message, owner, to_console)

    @property
    def get_service_name(self):
        return self.__class__.__name__

import datetime
import enum
import os
from pathlib import Path
from MasterApprenticeLib import TD1_Lib_MasterApprentice_Control
from MasterApprenticeLib.TD1_Lib_MasterApprentice_Control import MasterApprenticeLogVersionType, master_version_type, \
    master_logger_enabler, MAIN_DIR, delete_old_master_log
from MasterApprenticeLib.TD1_Lib_FileHandling import get_last_modified_time, delete_old_logs


"""
TwelfthDoctor1's Master Logger

The Master Logger is a custom logger used to log the happenings in a script.
"""

# User Defined Project Directory

MASTER_LOGGER_MAIN_DIR = None

main_dir = MASTER_LOGGER_MAIN_DIR if MASTER_LOGGER_MAIN_DIR is not None else MAIN_DIR


def get_log_dir():
    """
    Gets the Master Log File Directory.

    No Params Required.
    """

    log_name = "Master_Log.log"

    log_dir = os.path.join(main_dir, log_name)

    return log_dir


def get_new_log_dir():
    """
    Gets the Master Log File Directory for renaming.

    Existing Old Logs will be deleted if param: delete_old_master_log is set to True.

    No Params Required.
    """
    if delete_old_master_log is True:

        new_log_name = "Master_Log [OLD].log"

        new_log_dir = os.path.join(main_dir, new_log_name)

        if os.path.exists(new_log_dir):
            os.remove(new_log_dir)

            delete_old_logs(main_dir, "Master_Log [")

        return new_log_dir

    else:

        new_log_name = f"Master_Log [{get_last_modified_time(main_dir, 'Master_Log.log')}].log"

        new_log_dir = os.path.join(main_dir, new_log_name)

        return new_log_dir


if master_logger_enabler is True:
    if os.path.exists(get_log_dir()):
        os.rename(get_log_dir(), get_new_log_dir())

    with open(get_log_dir(), "w") as log_file:
        dt = datetime.datetime.now()
        log_file.write("TwelfthDoctor1's Master Log")
        log_file.write("\nApprentice Version: {0}".format(TD1_Lib_MasterApprentice_Control.__version__))
        log_file.write("\n==================================================================================================")
        log_file.write("\nCreation Date: {0} {1} {2} [UK] | {2} {1} {0} [US]".format(dt.day, dt.strftime("%B"), dt.year))
        log_file.write("\nCreation Time: {0}:{1}:{2} {3}".format(dt.strftime("%I"), dt.strftime("%M"), dt.strftime("%S"), dt.strftime("%p")))
        log_file.write("\n==================================================================================================")
        log_file.write("\nNEW LOG ENTRIES WILL BE APPENDED BELOW. ALL DATETIME WILL FOLLOW THE UK FORMAT.")
        log_file.write("\n==================================================================================================")
        log_file.write("\nMASTER LOG IS USED UNDER THE DIGRESSION OF TWELFTHDOCTOR1 UNDER THE USAGE OF DEBUG & TESTING.")
        log_file.write("\n==================================================================================================")
        log_file.close()


class MasterLogger:
    """
    The MasterLogger Class is a logger that logs the happenings of script when the specific functions are used.

    All logs from this class will be sent to Master_Log.log for analysis if needed.

    The MasterLogger should be used by TwelfthDoctor1 only.
    :param module_name
    :param main_owner
    :param additional_context
    """
    def __init__(self, module_name, main_owner=None, additional_context=None):
        self.module_name = module_name
        self.main_owner = main_owner
        self.addt_ctext = additional_context

    if master_logger_enabler is True:
        log_file = open(get_log_dir(), "a")

    def log(self, message, owner=None):
        """
        Logs the derived messaged onto MasterLog.
        Derived Message will be tagged as [LOG].
        :param message:
        :param owner:
        :return:
        """
        if master_logger_enabler is True:
            log_file = open(get_log_dir(), "a")
            dt_log = datetime.datetime.now()
            owner = self.main_owner or owner
            log_file.write("\n")
            log_file.write("\n[LOG: {0} {1} {2} | {3}:{4}:{5} {6}] {7} | {8}]".format(
                dt_log.day, dt_log.strftime("%B"),
                dt_log.year, dt_log.strftime("%I"),
                dt_log.strftime("%M"),
                dt_log.strftime("%S"),
                dt_log.strftime("%p"),
                self.module_name,
                owner
            ))
            if self.addt_ctext is not None:
                log_file.write("\n{0}".format(self.addt_ctext))
            log_file.write("\n")
            log_file.write("\n{0}".format(message))
            log_file.write("\n==================================================================================================")

    def info(self, message, owner=None):
        """
        Logs the derived message onto MasterLog.
        Derived Message will be tagged as [INFO].
        :param message:
        :param owner:
        :return:
        """
        if master_logger_enabler is True:
            log_file = open(get_log_dir(), "a")
            dt_info = datetime.datetime.now()
            owner = self.main_owner or owner
            log_file.write("\n")
            log_file.write("\n[INFO: {0} {1} {2} | {3}:{4}:{5} {6}] {7} | {8}]".format(
                dt_info.day, dt_info.strftime("%B"),
                dt_info.year, dt_info.strftime("%I"),
                dt_info.strftime("%M"),
                dt_info.strftime("%S"),
                dt_info.strftime("%p"),
                self.module_name,
                owner
            ))
            if self.addt_ctext is not None:
                log_file.write("\n{0}".format(self.addt_ctext))
            log_file.write("\n")
            log_file.write("\n{0}".format(message))
            log_file.write("\n==================================================================================================")

    def debug(self, message, owner=None):
        """
        Logs the derived message onto MasterLog.
        Derived Message will be tagged as [DEBUG].
        :param message:
        :param owner:
        :return:
        """
        if master_logger_enabler is True:
            log_file = open(get_log_dir(), "a")
            dt_debug = datetime.datetime.now()
            owner = self.main_owner or owner
            log_file.write("\n")
            log_file.write("\n[INFO: {0} {1} {2} | {3}:{4}:{5} {6}] {7} | {8}]".format(
                dt_debug.day, dt_debug.strftime("%B"),
                dt_debug.year, dt_debug.strftime("%I"),
                dt_debug.strftime("%M"),
                dt_debug.strftime("%S"),
                dt_debug.strftime("%p"),
                self.module_name,
                owner
            ))
            if self.addt_ctext is not None:
                log_file.write("\n{0}".format(self.addt_ctext))
            log_file.write("\n")
            log_file.write("\n{0}".format(message))
            log_file.write("\n==================================================================================================")

    def warn(self, message, owner=None):
        """
        Logs the derived message onto MasterLog.
        Derived Message will be tagged as [WARN].
        :param message:
        :param owner:
        :return:
        """
        if master_logger_enabler is True:
            log_file = open(get_log_dir(), "a")
            dt_warn = datetime.datetime.now()
            owner = self.main_owner or owner
            log_file.write("\n")
            log_file.write("\n[WARN: {0} {1} {2} | {3}:{4}:{5} {6}] {7} | {8}]".format(
                dt_warn.day, dt_warn.strftime("%B"),
                dt_warn.year, dt_warn.strftime("%I"),
                dt_warn.strftime("%M"),
                dt_warn.strftime("%S"),
                dt_warn.strftime("%p"),
                self.module_name,
                owner
            ))
            if self.addt_ctext is not None:
                log_file.write("{0}".format(self.addt_ctext))
            log_file.write("\n")
            log_file.write("\n{0}".format(message))
            log_file.write("\n==================================================================================================")

    def error(self, message, owner=None):
        """
        Logs the derived message onto MasterLog.
        Derived Message will be tagged as [ERROR].
        :param message:
        :param owner:
        :return:
        """
        if master_logger_enabler is True:
            log_file = open(get_log_dir(), "a")
            dt_error = datetime.datetime.now()
            owner = self.main_owner or owner
            log_file.write("\n")
            log_file.write("\n[ERROR: {0} {1} {2} | {3}:{4}:{5} {6}] {7} | {8}]".format(
                dt_error.day, dt_error.strftime("%B"),
                dt_error.year, dt_error.strftime("%I"),
                dt_error.strftime("%M"),
                dt_error.strftime("%S"),
                dt_error.strftime("%p"),
                self.module_name,
                owner
            ))
            if self.addt_ctext is not None:
                log_file.write("\n{0}".format(self.addt_ctext))
            log_file.write("\n")
            log_file.write("\n{0}".format(message))
            log_file.write("\n==================================================================================================")

    def assert_error(self, message, owner=None):
        """
        Logs the derived message onto MasterLog.
        Derived Message will be tagged as [ERROR WITH ASSERTION].

        USE WHEN NEEDED.
        :param message:
        :param owner:
        :return:
        """
        if master_logger_enabler is True:
            log_file = open(get_log_dir(), "a")
            dt_assert = datetime.datetime.now()
            owner = self.main_owner or owner
            log_file.write("\n")
            log_file.write("\n[ERROR WITH ASSERTION: {0} {1} {2} | {3}:{4}:{5} {6}] {7} | {8}]".format(
                dt_assert.day, dt_assert.strftime("%B"),
                dt_assert.year, dt_assert.strftime("%I"),
                dt_assert.strftime("%M"),
                dt_assert.strftime("%S"),
                dt_assert.strftime("%p"),
                self.module_name,
                owner
            ))
            if self.addt_ctext is not None:
                log_file.write("\n{0}".format(self.addt_ctext))
            log_file.write("\n")
            log_file.write("\n{0}".format(message))
            log_file.write("\n==================================================================================================")

            assert AssertionError(message)

    def exception(self, message, owner=None):
        """
        Logs the derived message onto MasterLog.
        Derived Message will be tagged as [EXCEPTION].
        :param message:
        :param owner:
        :return:
        """
        if master_logger_enabler is True:
            log_file = open(get_log_dir(), "a")
            dt_exc = datetime.datetime.now()
            owner = self.main_owner or owner
            log_file.write("\n")
            log_file.write("\n[ERROR: {0} {1} {2} | {3}:{4}:{5} {6}] {7} | {8}]".format(
                dt_exc.day, dt_exc.strftime("%B"),
                dt_exc.year, dt_exc.strftime("%I"),
                dt_exc.strftime("%M"),
                dt_exc.strftime("%S"),
                dt_exc.strftime("%p"),
                self.module_name,
                owner
            ))
            if self.addt_ctext is not None:
                log_file.write("\n{0}".format(self.addt_ctext))
            log_file.write("\n")
            log_file.write("\n{0}".format(message))
            log_file.write("\n==================================================================================================")

            assert Exception(message)

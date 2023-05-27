from UtilLib.Logging import LoggerClass


def exception_checker(func):
    """
    The Exception Checker is used to check for any Exceptions in the running code. If tripped, an error
    will be asserted and an Exception will occur.

    It is recommended to remove after testing as it may cause issues with function returners.

    To use this function, use the following method:
    @exception_checker
    def func():

    :param func: The function to be tested. (Can class be used?)
    :return: Exception Error or None
    """
    def inner_func(*args, **kwargs):
        exception_logger = LoggerClass(f"Exception Tracker @ {func.__name__}")

        try:
            # Try to execute the function
            func(*args, **kwargs)

        except Exception as e:
            # Except when an issue is detected which would trigger an exception
            # Exception is strictly vague to determine possible root cause
            exception_logger.warn(
                f"Exception has been detected in {func.__name__} with the following error:\n{e}"
            )

        else:
            # Inform that issue is fine
            exception_logger.info(
                f"No issues detected in {func.__name__}."
            )

        finally:
            # Returner
            return

    return inner_func

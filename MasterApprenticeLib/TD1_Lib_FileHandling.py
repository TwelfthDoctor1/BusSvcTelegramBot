import datetime
import enum
import os
from pathlib import Path


def get_last_modified_time(main_dir, log_name):
    """
    Get the last modified date and time from a file based
    on the file directory through epoch time and conversion.

    :param main_dir: Main Directory (named as main_dir)
    :param log_name: Name of the log in string (such as Master_Log.log)
    :return: Last modified time in actual time format
    """

    # Usage of epoch rounding should not allow it to go up by one second
    last_modt = round(os.path.getmtime(os.path.join(main_dir, log_name)), 0)

    dt_convert = datetime.datetime.fromtimestamp(float(last_modt))

    return dt_convert


def delete_old_logs(main_dir, starting_text):
    """
    Identifies files starting with a certain string and removes
    from the main directory.

    :param main_dir: Main Directory (named as main_dir)
    :param starting_text: An initial starting text common in all files following that name (Master_Log [~~~].log)
    :return: None
    """
    # x is File Directory
    # y is Sub File Directories in the Directory in List form
    # z is Files in theDirectory in List form
    # i is the individual file derived from z

    for (x, y, z) in os.walk(main_dir):
        for i in z:

            # Any files that start with the starting text will be deleted
            if str(i).startswith(starting_text):
                os.remove(os.path.join(main_dir, i))

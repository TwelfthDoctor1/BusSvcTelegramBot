import urllib.error
import urllib.request
from UtilLib.Logging import LoggerClass


# TEST URL
TEST_URL = "https://google.com"

# urllib Handling
TEST_REQUEST = urllib.request.Request(url=TEST_URL, method="GET")

# LOGGER FOR TEST
NETWORK_LOGGER = LoggerClass("Network Test Logger")


def network_test():
    """
    A function that makes use of urllib to test whether the computer is connected to the internet.

    :return: True/False
    """
    try:
        with urllib.request.urlopen(TEST_REQUEST) as response:
            return True

    except urllib.error.URLError as e:
        NETWORK_LOGGER.info(
            "Cannot connect to internet. Any internet related functions will be disabled."
        )

        if hasattr(e, "code") and hasattr(e, "reason"):
            # HTTP Error Code + Reason
            NETWORK_LOGGER.error(f"HTTP ERROR CODE {e.code} | {e.reason}")

        elif hasattr(e, "reason"):
            # HTTP Error Reason
            NETWORK_LOGGER.error(f"FAILURE REASON | {e.reason}")

        else:
            # Exception Error Dump
            NETWORK_LOGGER.error(f"RAW FAILURE REASON | {e}")

        return False

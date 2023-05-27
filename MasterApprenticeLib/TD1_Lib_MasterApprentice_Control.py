from pathlib import Path

# Main Path File for Project
# Set .parent level if MasterApprentice Library is nested
MAIN_DIR = Path(__file__).resolve().parent.parent


class MasterApprenticeLogVersionType:
    DEVELOPER = 0
    BETA = 1
    RELEASE = 2


# Authoring, Attributes and Licensing
__author__ = "TwelfthDoctor1"
__copyright__ = "Copyright 2020: MasterApprentice Logger Project | © TD1 & TWoCC 2020-2022"
__credits__ = "TwelfthDoctor1"
__license__ = "CC 4.0 or MIT"

# Version Control Datum
__version__ = "Developer Version 1.3.0"
__status__ = "Development Testing"


# The Version Type of Master Apprentice Logger
master_version_type = MasterApprenticeLogVersionType.DEVELOPER
apprentice_version_type = MasterApprenticeLogVersionType.DEVELOPER

# Enabler for the Master Logger
# Leave this as [False] for release versions
master_logger_enabler = True

# Delete old ApprenticeLogger Logs
delete_old_apprentice_log = True

# Delete old MasterLogger Logs
delete_old_master_log = True

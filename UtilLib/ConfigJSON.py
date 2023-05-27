# ======================================================================================================================
# Module Importation
from pathlib import Path
from sys import platform
from UtilLib.JSONHandler import JSONHandler, JSON_LIB

# ======================================================================================================================
# Default Config File Format
# This Dictionary consists of the default keys & values for the Config File to use on generation.
CONFIG_DEFAULT = {
    "database_dir_win32": "~",
    "database_dir_macos": "~",
    "database_dir_linux": "~",
    "database_sheet_name": "Database",
    "frame_cycles": 100
}


# ======================================================================================================================
# ConfigJSON Class
class ConfigJSON(JSONHandler):
    """
    A Configuration Handler that borrows functions from JSONHandler.
    """
    def __init__(self):
        """
        Initialise the ConfigJSON Class & generate the Config file if required.
        """
        super(ConfigJSON, self).__init__("Database_Config", Path(JSON_LIB).resolve().parent)
        self.generate_config()

    def generate_config(self):
        """
        Generate the Config JSON. Avoids usage of generate_json().
        :return:
        """
        # Generate Config
        status = self.generate_json(CONFIG_DEFAULT)

        # Key Check on Existing Config
        if status is False:
            key_check_list = list(self.json_data.keys())
            for key_def in CONFIG_DEFAULT.keys():
                for key_check in key_check_list:
                    if key_def == key_check:
                        key_check_list.remove(key_check)

            # Add missing keys
            if len(key_check_list) > 0:
                self.logger.info(f"Config Check: {len(key_check_list)} keys missing. Appending...\n\n{key_check_list}")

                for key in key_check_list:
                    self.json_data[key] = CONFIG_DEFAULT[key]
            else:
                self.logger.info(f"Config Check: All keys accounted for. No key appending required.")

    def getExcelPath(self):
        """
        All in one method of getting Excel FP based on platform type.

        Avoids repeated usage of return_specific_json().

        :return:
        """
        if platform == "win32":
            return self.return_specific_json("database_dir_win32")
        elif platform == "darwin":
            return self.return_specific_json("database_dir_macos")
        else:
            return self.return_specific_json("database_dir_linux")

    def updateExcelPath(self, fp: Path or str):
        """
        All in one method of updating Excel FP based on platform type.

        Avoids repeated usage of update_specific_json().

        :param fp: The filepath of the Excel Database File. Can be in str or in Path.
        :return:
        """
        # Change Filepath
        if platform == "win32":
            self.update_specific_json("database_dir_win32", fp)
        elif platform == "darwin":
            self.update_specific_json("database_dir_macos", fp)
        else:
            self.update_specific_json("database_dir_linux", fp)

        # Update JSON File
        self.update_json_file()

    def getConfigData(self):
        """
        Alternate call method to get Config Data.

        :return:
        """
        self.formulate_json()

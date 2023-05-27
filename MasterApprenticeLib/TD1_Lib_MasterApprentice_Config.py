import os
import configparser
from pathlib import Path
from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger
from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger
from MasterApprenticeLib.TD1_Lib_MasterApprentice_Control import __version__, __copyright__
from MasterApprenticeLib.TD1_Lib_ConsoleHandling import clear_console
import time

apprentice_logger = ApprenticeLogger('TD1 MasterApprentice Logger Config', main_owner='TwelfthDoctor1')
master_logger = MasterLogger('TD1 MasterApprentice Logger Config', main_owner='TwelfthDoctor1')

# Settings
# All options should mirror that of Control Module

# Configuration Keys
# Used to identify Config Options
config_key_list = [
    "master_logger_enabler",
    "delete_old_apprentice_log",
    "delete_old_master_log",
    "test_int",
    "test_dec",
    "test_str",
    "test_string"
]

# Configuration Values
# Used to determine said Option holds what value
preset_modifiers = [
    "False",
    "False",
    "False",
    "1",
    "2.4",
    "Test",
    "value"
]

# Notif Changed Dialog Determiner
# Set True for Must Restart, Set False for Non-Restart [In Bool, not Str]
dialog_determiner = [
]


main_dir = Path(__file__).resolve().parent

config = configparser.ConfigParser()

main_header = 'TD1 MasterApprentice Logger Config Settings'


def get_config_dir():
    """
    Gets the Configuration File Directory.

    No Params Required.
    """

    log_name = "TD1_MasterApprentice_Settings.cfg"

    config_dir = os.path.join(main_dir, log_name)

    return config_dir


def config_prep_file():
    """
    Configures and creates a brand new Config File for use.
    :return:
    """
    with open(get_config_dir(), "w") as config_file:
        config_file.write("[TD1 MasterApprentice Logger Config Settings]")
        # Incrementor Int by default is presumed as 0 and increments from there.
        # List Assigns start off as 0 as well.
        for incrementor in range(len(config_key_list)):
            config_file.write("\n" + config_key_list[incrementor] + " = " + preset_modifiers[incrementor])

        config_file.close()


def config_data_test(data):
    """
    This function is a test to determine the data type.
    :param data:
    :return:
    """

    if data == "True" or data == "False":
        return True

    else:
        return False


def config_data_get(config_func, header, key):
    """
    This function is the configuration all-in-one get handler.
    If the specified value is:

    boolean -> return True/False
    integer -> Numbers
    float -> Decimal Numbers
    else -> Use as String
    :param config_func:
    :param header:
    :param key:
    :return:
    """
    data = config_func.get(header, key)

    if data == "True" or data == "False":
        return config.getboolean(header, key)

    elif data.isnumeric():
        return config.getint(header, key)

    elif is_float_str(data):
        return config.getfloat(header, key)

    else:
        return config.get(header, key)


if os.path.exists(get_config_dir()) is True:
    with open(get_config_dir(), "r") as config_file:
        config.read_file(config_file)

        apprentice_logger.info("TD1 DevAccessPanel Config File Found.", owner="TwelfthDoctor1")

        master_logger.info("TD1 DevAccessPanel Config File Found.", owner="TwelfthDoctor1")

else:
    config_prep_file()
    with open(get_config_dir(), "r") as config_file:
        config.read_file(config_file)

        apprentice_logger.info("TD1 DevAccessPanel Config File Missing. Creating New Config File...",
                               owner="TwelfthDoctor1")

        master_logger.info("TD1 DevAccessPanel Config File Missing. Creating New Config File...",
                           owner="TwelfthDoctor1")


def print_config_values():
    with open(get_config_dir(), "r") as config_file:
        config.read_file(config_file)
        for incrementor in range(len(config_key_list)):
            value = config.get(main_header, config_key_list[incrementor])
            print("{}: {}".format(config_key_list[incrementor], value))


def print_config_values_ui():
    with open(get_config_dir(), "r") as config_file:
        config.read_file(config_file)
        for incrementor in range(len(config_key_list)):
            value = config.get(main_header, config_key_list[incrementor])
            print(f"[{incrementor + 1}] {config_key_list[incrementor]}: {value}")


def check_modifier_status(status):
    if status is True:
        result = "ENABLED"
        return result
    else:
        result = "DISABLED"
        return result


def set_option(option):
    returner = False
    clear_console()

    if get_option_value(config_key_list[int(option) - 1]) is True or get_option_value(config_key_list[int(option) - 1]) is False:
        # Option for Boolean
        input_bool = "y"

        print("======================================================================================================")
        print(f"[{option}] {config_key_list[int(option) - 1]}")
        print(f"Currently: {get_option_value(config_key_list[int(option) - 1])}")

        while input_bool.lower() == "y" or input_bool.lower() == "n":
            input_bool = input(f"Do you want to set {config_key_list[int(option) - 1]} to {not get_option_value(config_key_list[int(option) - 1])}? [Y/n]: ")

            if input_bool == "n":
                print("======================================================================================================")
                print("Exiting...")
                break

            if not (input_bool.lower() == "y" or input_bool.lower() == "n"):
                print("======================================================================================================")
                print("Input Invalid, please input a correct value.")
                continue

            returner = option_toggle(int(option) - 1)

            if returner is True:
                return

    elif str(get_option_value(config_key_list[int(option) - 1])).isdecimal():
        # Option for Numeric
        input_int = "1"

        print("======================================================================================================")
        print(f"[{option}] {config_key_list[int(option) - 1]}")
        print(f"Currently: {get_option_value(config_key_list[int(option) - 1])}")

        while input_int.isnumeric():
            input_int = input(f"Enter a integer value: ")

            if input_int.isnumeric() is False:
                print("======================================================================================================")
                print("Input Invalid, please input a correct value.")
                continue

            returner = option_toggle(int(option) - 1, input_int)

            if returner is True:
                return

    elif is_float_str(str(get_option_value(config_key_list[int(option) - 1]))):
        # Option for Decimal
        input_dec = "1.3"

        print("======================================================================================================")
        print(f"[{option}] {config_key_list[int(option) - 1]}")
        print(f"Currently: {get_option_value(config_key_list[int(option) - 1])}")

        while is_float_str(input_dec):
            input_dec = input(f"Enter a decimal value: ")

            if is_float_str(input_dec) is False:
                print("======================================================================================================")
                print("Input Invalid, please input a correct value.")
                continue

            returner = option_toggle(int(option) - 1, input_dec)

            if returner is True:
                return

    else:
        # Option for String
        input_str = "~"

        print("======================================================================================================")
        print(f"[{option}] {config_key_list[int(option) - 1]}")
        print(f"Currently: {get_option_value(config_key_list[int(option) - 1])}")

        while input_str != "":
            input_str = input(f"Enter a string value: ")

            if input_str == "":
                print("======================================================================================================")
                print("Input Invalid, please input a correct value.")
                continue

            returner = option_toggle(int(option) - 1, input_str)

            if returner is True:
                return


def config_init_check():
    """
    Runs an initial check on the config file for any missing options.
    Prudent on newer versions with config implementations.
    :return:
    """
    with open(get_config_dir(), "r") as config_file:
        config.read_file(config_file)
        for incrementor in range(len(config_key_list)):
            if config.has_option(main_header, config_key_list[incrementor]) is False:
                append_option(incrementor)

        apprentice_logger.info("Config List Check Success.", owner="TwelfthDoctor1")

        master_logger.info("Config List Check Success.", owner="TwelfthDoctor1")


def append_option(identifier):
    """
    Appends missing options into the config file.
    :param identifier:
    :return:
    """
    option = config_key_list[identifier]
    modifier = preset_modifiers[identifier]
    with open(get_config_dir(), "a") as config_file:
        config_file.write("\n" + option + " = " + modifier)
        config_file.close()

        apprentice_logger.info("Option Key: {0} has been appended into Config File.".format(option),
                               owner="TwelfthDoctor1")

        master_logger.info("Option Key: {0} has been appended into Config File.".format(option),
                           owner="TwelfthDoctor1")

    with open(get_config_dir(), "r") as config_file:
        return config_file


config_init_check()


def boolean_not_converter(state):
    if state is True:
        return "False"
    else:
        return "True"


def option_toggle(identifier, to_set:str=""):
    option = config_key_list[identifier]

    if config.has_option(main_header, option) is False:
        append_option(identifier)
    else:
        with open(get_config_dir(), "r") as config_file:
            config.read_file(config_file)
            setting_value = config_data_get(config, main_header, option)
            print("{0} {1}".format(option, setting_value))

            if setting_value is True:
                value = "False"
                config.set(main_header, option, value)
                config.write(open(get_config_dir(), "w"))

            elif setting_value is False:
                value = "True"
                config.set(main_header, option, value)
                config.write(open(get_config_dir(), "w"))

            else:
                value = to_set
                config.set(main_header, option, value)
                config.write(open(get_config_dir(), "w"))

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info(
                "Option: {0} has been set to {1}. (Formerly {2})".format(option, value, setting_value),
                owner="TwelfthDoctor1")

        if master_logger is not None and master_logger is not False:
            master_logger.info("Option: {0} has been set to {1}. (Formerly {2})".format(option, value, setting_value),
                               owner="TwelfthDoctor1")

        dialog_message = f"The option: {option} has been changed from {setting_value} to {value}."

        print("======================================================================================================")
        print(dialog_message)
        input("Press [Enter] to continue...")

        return True


def get_option_value(option):
    """
    Gets the value from the option (key) in the Config List.
    :param option:
    :return:
    """
    with open(get_config_dir(), "r") as config_file:
        config.read_file(config_file)
        data = config.get(main_header, option)

        if data == "True" or data == "False":
            return config.getboolean(main_header, option)

        elif data.isnumeric():
            return config.getint(main_header, option)

        elif is_float_str(data):
            return config.getfloat(main_header, option)

        else:
            return config.get(main_header, option)


def config_exist(option):
    for key in config_key_list:
        if key == option:
            return True

    return False


def return_option_count():
    return len(config_key_list)


def config_ui_init():
    """
    Main UI Method used to call the MasterApprentice Logger
    Settings UI.
    """
    option = "1"
    returner = False

    while option != "0" or option.lower() == "q":
        clear_console()

        print("======================================================================================================")
        print("TwelfthDoctor1's MasterApprentice Logger Settings")
        print(__copyright__)
        print(__version__)
        print("======================================================================================================")

        # Print Config List - UI Form
        print_config_values_ui()

        print("======================================================================================================")
        print(f"Enter a value of 1 to {return_option_count()} to change that option.")
        print("Or input 0 or Q to exit Config Settings.")
        print("======================================================================================================")
        option = input("Option: ")

        if option == "0" or option.lower() == "q":
            print("======================================================================================================")
            print("Exiting...")
            time.sleep(2)
            break

        if is_float_str_0(option) and int(option) > return_option_count():
            print("======================================================================================================")
            print("Input Invalid, please input a correct value.")
            continue

        set_option(option)


def is_float_str(value):
    value = value.replace(" ", "_")

    if value.isalpha():
        return False

    int_value = round(float(value), 0)

    r = float(value) - int_value

    if 0 <= r < 1:
        return True

    else:
        return False


def is_float_str_0(value):
    value = value.replace(" ", "_")

    if value.isalpha():
        return False

    int_value = round(float(value), 0)

    r = float(value) - int_value

    if 0 < r < 1:
        return True

    else:
        return False

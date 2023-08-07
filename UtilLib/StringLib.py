

# ONE CHAR CHECKLIST - NUMBERS & LETTERS
UPPERCASE_LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                     "U", "V",  "W", "X", "Y", "Z"]
LOWERCASE__LETTERS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
                      "t", "u", "v",  "w", "x", "y", "z"]
NUMBERS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


def check_startswith(value: str, check: []):
    """
    Checks whether the string value starts with any value specified in the checklist.
    :param value: String value to be checked in str
    :param check: checklist of string words in [str, ...]
    :return: bool True/False
    """
    for check_val in check:
        if value.startswith(check_val):
            return True

    return False


def check_endswith(value: str, check: []):
    """
    Checks whether the string value ends with any value specified in the checklist.
    :param value: String value to be checked in str
    :param check: checklist of string words in [str, ...]
    :return: bool True/False
    """
    for check_val in check:
        if value.endswith(check_val):
            return True

    return False


def end_split(value: str, check: []):
    """
    Splits the string value if the string ends with any value specified in the checklist.
    :param value: String value to be checked in str
    :param check: checklist of string words in [str, ...]
    :return: Spilt Value in str [str, str, ...]
    """
    for check_val in check:
        if value.endswith(check_val):
            return value.split(check_val)


def to_pascal_case(string: str, sep: str or None = None):
    str_list = string.split(sep)

    for i in range(len(str_list)):
        str_list[i] = str_list[i].capitalize()

    if sep is None:
        returner = " ".join(str_list)
    else:
        returner = sep.join(str_list)

    return returner


def to_camel_case(string: str, sep: str or None = None):
    str_list = string.split(sep)

    for i in range(len(str_list)):
        if i == 0:
            continue

        str_list[i] = str_list[i].capitalize()

    if sep is None:
        returner = " ".join(str_list)
    else:
        returner = sep.join(str_list)

    return returner

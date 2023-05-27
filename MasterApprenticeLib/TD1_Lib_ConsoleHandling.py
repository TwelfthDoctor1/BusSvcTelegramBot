import os


def clear_console():
    """
    Clears the Terminal Console to clean up old UI Menus.
    """
    return os.system("cls" if os.name == "nt" else "clear")

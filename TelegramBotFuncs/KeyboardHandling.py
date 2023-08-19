from telebot import types


def start_menu_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    kb.add(
        types.KeyboardButton("Query Timing"),
        # types.KeyboardButton("Search"),
        types.KeyboardButton("Refresh"),
        types.KeyboardButton("Filter"),
        types.KeyboardButton("Cancel"),
        types.KeyboardButton("Clear"),
        types.KeyboardButton("Add to Favourites"),
        types.KeyboardButton("Favourites"),
        types.KeyboardButton("Delete from Favourites"),
        types.KeyboardButton("Settings")
    )

    return kb


def keypad_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    kb.add(
        types.KeyboardButton("1"),
        types.KeyboardButton("2"),
        types.KeyboardButton("3"),
        types.KeyboardButton("4"),
        types.KeyboardButton("5"),
        types.KeyboardButton("6"),
        types.KeyboardButton("7"),
        types.KeyboardButton("8"),
        types.KeyboardButton("9"),
        types.KeyboardButton("√"),
        types.KeyboardButton("0"),
        types.KeyboardButton("X"),
        types.KeyboardButton("Cancel")
    )

    return kb


def handle_keypad_response(text: str, max_str: int = -1):
    if text[-1] == "X":
        return False, ""

    elif text[-1] == "√":
        return True, text

    elif len(text) == max_str and max_str > 0:
        return True, text


def option_keyboard(msg: iter, row_size: int = 1):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=row_size)
    for i in range(len(msg)):
        kb.add(types.KeyboardButton(f"[{i + 1}] {msg[i]}"))

    kb.add(types.KeyboardButton("Cancel"))

    return kb


def get_option_number(text: str, msg: iter):
    for i in range(len(msg)):
        if text.strip().find(f"[{i + 1}] {msg[i]}".strip()) != -1:
            print(f"{text} | [{i + 1}] {msg[i]}")
            return i + 1


def location_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    kb.add(
        types.KeyboardButton("Send Location", request_location=True),
        types.KeyboardButton("Cancel")
    )

    return kb


def cancel_only_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    kb.add(
        types.KeyboardButton("Cancel")
    )

    return kb


def filtering_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    kb.add(
        types.KeyboardButton("No Filtering"),
        types.KeyboardButton("Cancel")
    )

    return kb


def destroy_keyboard():
    return types.ReplyKeyboardRemove()

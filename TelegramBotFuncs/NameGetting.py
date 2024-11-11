from telebot import types


def get_user_name(message: types.Message):
    if message.from_user.username is not None:
        return message.from_user.username
    elif message.from_user.full_name:
        return message.from_user.full_name
    else:
        return None

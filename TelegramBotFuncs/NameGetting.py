from telebot import types


def get_user_name(message: types.Message):
    if message.from_user.username is not None:
        return message.from_user.username
    else:
        return message.from_user.full_name

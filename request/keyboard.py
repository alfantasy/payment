from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

register = InlineKeyboardMarkup()
register_0 = InlineKeyboardButton(text="Зарегистрироваться", callback_data="send_register")
register.add(register_0)

continue_because_register = InlineKeyboardMarkup()
continue_because_register_0 = InlineKeyboardButton(text="Продолжить", callback_data="next_because_register")
continue_because_register.add(continue_because_register_0)
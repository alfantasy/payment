from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

register = InlineKeyboardMarkup()
register_0 = InlineKeyboardButton(text="Зарегистрироваться", callback_data="send_register")
register.add(register_0)

continue_because_register = InlineKeyboardMarkup()
continue_because_register_0 = InlineKeyboardButton(text="Продолжить", callback_data="next_because_register")
continue_because_register.add(continue_because_register_0)

bought_film = InlineKeyboardMarkup()
bought_film_0 = InlineKeyboardButton(text="Покупка доступа", callback_data="buy_access")
bought_film.add(bought_film_0)

buying_access = InlineKeyboardMarkup()
buying_access_0 = InlineKeyboardButton(text="Оплата", callback_data="buying_access")
buying_access.add(buying_access_0)

def claim_keybaord(url_redict):
    keyboard = InlineKeyboardMarkup()
    keyboard0 = InlineKeyboardButton(text="Перейти к оплате", url=url_redict)
    keyboard1 = InlineKeyboardButton(text="Проверить оплату", callback_data="check_donate")
    keyboard.add(keyboard0)
    keyboard.add(keyboard1)
    return keyboard
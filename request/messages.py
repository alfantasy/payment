def profile(id, name, status, bought):
    user_status = ''
    if status == 1:
        if bought == 1:
            user_status = 'Оплачен.'
        else:
            user_status = "Проверьте статус оплаты"
    if bought == 0 and status == 0:
        user_status = f'Неоплачен.'
    message = f"""
Ваш ID: {id}
Ваш никнейм: {name}
Статус: {user_status}
"""
    return message

def buy_access(name):
    message = f"""
{name}, 🎄Что бы посмотреть все серии сериала необходимо оплатить за вход 150 руб🎄
После оплаты мы сразу же дадим ссылку на канал с сериями! ❄️
P.S. Доступ к каналу неограничен🫂. Подписка дается навсегда! <3   
"""
    return message
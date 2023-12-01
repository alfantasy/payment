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
from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, InputFile, InputMedia, CallbackQuery
from aiogram.utils.callback_data import CallbackData
from aiogram.types.message import ContentType
import logging 
import string
import random
from yoomoney import Quickpay, Client
from config import token_p2p
import time
import request.keyboard as ckeyboard
import request.messages as cmessages

tg_token = "6861833485:AAEmXlv5tEjCPXB-Lg1aOCxLAWHnjFvigeY"

url_for_channel = "https://t.me/+4t5sFE-3QKUwZjAy"
bot = Bot(token=tg_token)
dp = Dispatcher(bot)
cb = CallbackData("btn", "action")

admins = [1050898927]

logger = logging.getLogger('log')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('overspj.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

class User:
    def __init__(self,id,tgname,tgid,payment_status,bought, label_status):
        self.id = id
        self.tgid = tgid
        self.tgname = tgname 
        self.payment_status = payment_status
        self.bought = bought
        self.label_status = label_status

def save_database(users):
    lines = []
    for user in users: 
        lines.append(f'"id" : {user.id}, "tgid" : "{user.tgid}", "tgname" : "{user.tgname}", "payment_status" : {user.payment_status}, "bought" : {user.bought}, "label_status" : "{user.label_status}"')
    lines = '\n'.join(lines)
    with open("base.txt", 'w', encoding='utf-8') as file: 
        file.write(lines)
        file.close()

def read_database():
    users = []
    with open("base.txt", 'r', encoding='utf-8') as file: 
        lines = [x.replace('\n', '') for x in file.readlines()]
        file.close()
    for line in lines:
        line = eval('{' + line + '}')
        if line != '{}':
            users.append(User(id = line['id'], tgid = line['tgid'], tgname = line['tgname'], payment_status = line['payment_status'], bought = line['bought'], label_status = line['label_status']))
    return users  

def new_user(userid, tg, nick):
    file = open("base.txt", "a")
    users.append(User(userid, tg, nick, 0, 0, "no"))
    file.close()

users = read_database()

@dp.message_handler(commands=['test'])
async def test(message: types.Message):
    print("Посылаю сообщения администратору канала.")
    await bot.send_message(admins[0], "проверка связи.")

@dp.message_handler(commands=['start'])
async def now_start(message: types.Message):
    users = read_database()
    xx = open('base.txt', 'r', encoding='utf-8')
    x = xx.read()
    xx.close()
    await bot.send_message(message.from_user.id, " Проверка регистрации! ")
    time.sleep(5)
    if (str(message.from_user.id) in x):
        await bot.send_message(message.from_user.id, "Вы и так зарегистированы.")
        users = read_database()
        for user in users:
            if message.from_user.id == user.id:
                await bot.send_message(message.from_user.id, cmessages.profile(message.from_user.id, message.from_user.first_name, user.payment_status, user.bought), reply_markup=ckeyboard.bought_film)
    else:
        await bot.send_message(message.from_user.id, " Вы не найдены в системе. Регистрируемся?", reply_markup=ckeyboard.register)

@dp.message_handler(commands=['profile'])
async def profile_send(message: types.Message):
    users = read_database()
    xx = open('base.txt', 'r', encoding='utf-8')
    x = xx.read()
    xx.close()
    if (str(message.from_user.id) in x):
        for user in users:
            if message.from_user.id == user.id:
                await bot.send_message(message.from_user.id, cmessages.profile(message.from_user.id, message.from_user.first_name, user.payment_status, user.bought), reply_markup=ckeyboard.bought_film)
    else:
        await bot.send_message(message.from_user.id, "Вы не найдены в системе. Регистрируемся?", reply_markup=ckeyboard.register)

@dp.callback_query_handler(run_task=lambda call: True)
async def callback_keyboard(call: CallbackQuery):
    cuser_id = call.message.chat.id 
    cuser_name = call.from_user.first_name
    if call.data == "send_register":
        await bot.send_message(cuser_id, "Вы успешно зарегистрированы в системе. Нажмите кнопку <Продолжить>", reply_markup=ckeyboard.continue_because_register)
        new_user(cuser_id, call.from_user.first_name, call.from_user.username)
        save_database(users)
    if call.data == "next_because_register":
        for user in users:
            if cuser_id == user.id:
                await bot.send_message(cuser_id, cmessages.profile(cuser_id, cuser_name, user.payment_status, user.bought), reply_markup=ckeyboard.bought_film)
    if call.data == "buy_access":
        for user in users: 
            if cuser_id == user.id:
                await bot.send_message(cuser_id, cmessages.buy_access(cuser_name), reply_markup=ckeyboard.buying_access)
    if call.data == "buying_access":
        for user in users:
            if cuser_id == user.id:
                letters_and_digits = string.ascii_lowercase + string.digits
                rand_string = ''.join(random.sample(letters_and_digits, 10))
                quickpay = Quickpay(
                    receiver='4100118465877733',
                    quickpay_form="shop",
                    targets='SlovoPatsana',
                    paymentType="SB",
                    sum=150,
                    label=rand_string
                )                

                user.label_status = rand_string
                save_database(users)

                await bot.send_message(call.from_user.id, "Покупка производится через сервис ЮMoney, все транкзации легетивны. После оплаты, нажмите на кнопку <Проверить оплату>", reply_markup=ckeyboard.claim_keybaord(quickpay.redirected_url))         
    if call.data == "check_donate":
        for user in users: 
            if call.from_user.id == user.id:
                bought = user.bought
                label = user.label_status
                status = user.payment_status
                id_user = user.id
        if bought == 0:
            client = Client(token_p2p)
            history = client.operation_history(label=label)
            try:
                operation = history.operations[-1]
                if operation.status == "success":
                    for user in users:
                        if call.from_user.id == user.id:
                            user.bought = 1
                            user.payment_status = 1
                            save_database(users)
                            await bot.send_message(call.from_user.id, "Оплата проведена успешно. Ожидайте ссылки на канал")
                            time.sleep(5)
                            await bot.send_message(call.from_user.id, f"Вот ваша ссылка на канал: {url_for_channel}")
                    await bot.send_message(admins[0], f"Пользователь @{call.from_user.username} с ником {cuser_name} совершил покупку. Подтвердите его заявку в группу.")
                    await bot.send_message(admins[0], f"Если в сообщении после @ указано None, значит у пользователя нет юзер-нейма. Ориентируйтесь по нику.")
            except:
                await bot.send_message(call.from_user.id, "Ожидайте, когда оплата пройдет. Уведомление придет.")
        else:
            await bot.send_message(call.from_user.id, "Покупка присваивается лишь конкретному пользователю. \nВы уже оплатили подписку.")

executor.start_polling(dp, skip_updates=True)  
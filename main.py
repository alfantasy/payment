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

tg_token = "6442408751:AAEQTJhHCRCBLZ6VGurMNGBz8zb6Ceh3Jc4"
tg_token_payments = "381764678:TEST:72571"

PRICE = types.LabeledPrice(label="Подписка на 1 месяц", amount=500*100)

bot = Bot(token=tg_token)
dp = Dispatcher(bot)
cb = CallbackData("btn", "action")

logger = logging.getLogger('log')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('overspj.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

class User:
    def __init__(self,id,tgname,payment_status,bought):
        self.id = id
        self.tgname = tgname 
        self.payment_status = payment_status
        self.bought = bought

def save_database(users):
    lines = []
    for user in users: 
        lines.append(f'"id" : {user.id}, "tgname" : "{user.tgname}", "payment_status" : {user.payment_status}, "bought" : {user.bought}')
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
            users.append(User(id = line['id'], tgname = line['tgname'], payment_status = line['payment_status'], bought = line['bought']))
    return users  

def new_user(userid, nick):
    file = open("base.txt", "a")
    users.append(User(userid, nick, 0, 0))
    file.close()

users = read_database()

@dp.message_handler(commands=['buy'])
async def buy(message: types.Message):
    letters_and_digits = string.ascii_lowercase + string.digits
    rand_string = ''.join(random.sample(letters_and_digits, 10))
    quickpay = Quickpay(
        receiver='4100117067201070',
        quickpay_form="shop",
        targets='Test',
        paymentType="SB",
        sum=2,
        label=rand_string
    )

    claim_keyboard = InlineKeyboardMarkup()
    claim_keyboard.add(InlineKeyboardButton(text="Перейти к оплате!", url=quickpay.redirected_url))
    claim_keyboard.add(InlineKeyboardButton(text='Получить товар!', callback_data="btn:claim"))

    await bot.send_message(message.from_user.id, "Производим оплату!", reply_markup=claim_keyboard)

@dp.message_handler(commands=['start'])
async def now_start(message: types.Message):
    users = read_database()
    xx = open('base.txt', 'r', encoding='utf-8')
    x = xx.read()
    xx.close()
    await bot.send_message(message.from_user.id, " Проверка регистрации")
    time.sleep(5)
    if (str(message.from_user.id) in x):
        await bot.send_message(message.from_user.id, "Вы и так зарегистированы.")
    else:
        await bot.send_message(message.from_user.id, " Вы не найдены в системе. Регистрируемся?", reply_markup=ckeyboard.register)

@dp.callback_query_handler(run_task=lambda call: True)
async def callback_keyboard(call: CallbackQuery):
    cuser_id = call.message.chat.id 
    cuser_name = call.from_user.first_name
    if call.data == "send_register":
        await bot.send_message(cuser_id, "Вы успешно зарегистрированы в системе. Нажмите кнопку <Продолжить>", reply_markup=ckeyboard.continue_because_register)
        new_user(cuser_id, call.from_user.username)
        save_database(users)
    if call.data == "next_because_register":
        for user in users:
            if cuser_id == user.id:
                await bot.send_message(cuser_id, cmessages.profile(cuser_id, cuser_name, user.payment_status, user.bought))


@dp.callback_query_handler(cb.filter(action="claim"))
async def check_payment(call: CallbackQuery):
   client = Client(token_p2p)
   history = client.operation_history(label=slabel)
   try:
        operation = history.operations[-1]
        if operation.status == "success":
            await bot.send_message(call.message.chat.id, "Успешно")
   except: 
        await bot.send_message(call.message.chat.id, "Ждите")
    

executor.start_polling(dp, skip_updates=True)  
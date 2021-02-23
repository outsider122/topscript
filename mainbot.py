import json
import random
import sqlite3
import requests
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup


bot_token = '1668667352:AAFrZwLvR7j7ma-pKdFVPLpIH-D4Az27EcU' 

bot = Bot(token=bot_token)

dp = Dispatcher(bot, storage=MemoryStorage())

publick_key = '48e7qUxn9T7RyYE1MVZswX1FRSbE6iyCj2gCRwwF3Dnh5XrasNTx3BGPiMsyXQFNKQhvukniQG8RTVhYm3iPvYSzQ64FZjixcDeu2q7hHfro7svdtjdhNuH22R3XtCDyEfheNTshUv9AwP6mc9sAj43p8AP89K2v33JEM6STfm8aDF7xagDERR92MBDnx' 

token = 'aa83a01cd8b3d5c0bfebcc48dc161b0b' 

phone = '+380974845941' 

help_message = '''Техническая поддержка:\n@favorit_betting'''

admins = [1546170311,1464117623,1412541991]

card = '4890494729256032' #карта на оплату

cardua = '4890494729256032'

start_message = """
🎉Привет, {}

Политика и условия пользования данным ботом:
1. Играя у нас, вы берёте все риски за свои средства на себя.
2. Принимая правила, Вы подтверждаете своё совершеннолетие!
3. Ваш аккаунт может быть забанен в подозрении на мошенничество/обман нашей системы!
4. Мультиаккаунты запрещены!
5. Скрипты, схемы использовать запрещено!
6. Если будут выявлены вышеперчисленные случаи, Ваш аккаунт будет заморожен до выяснения обстоятельств!
7. В случае необходимости администрация имеет право запросить у Вас документы, подтверждающие Вашу личность и Ваше совершеннолетие.
MoneyBot
Вы играете на виртуальные монеты, покупая их за настоящие деньги. Любое пополнение бота является пожертвованием!  Вывод денежных средств осуществляется только при достижении баланса, в 5 раз превышающего с сумму Вашего пополнения!По всем вопросам Вывода средств, по вопросам пополнения, а так же вопросам играм обогащайтесь в поддержку, указанную в описании к боту. Пишите сразу по делу, а не «Здравствуйте! Тут?»
Старайтесь изложить свои мысли четко и ясно, что поддержка не мучалась и не пыталась Вас понять.
Спасибо за понимание!
Удачи в игре.
Ваша задача - угадать, в каком диапазоне будет располагаться выпадшее число. 
От 0 до 50, либо от 50 до 100, в таком случае Вы получаете удовение суммы ставки, либо же если Ваше число будет равно 50, то тогда Вы получаете выигрыш равный 10 Вашим ставкам. Но вероятность выпадения данного числа намного ниже.

Удачи!
"""

profile_button = types.KeyboardButton('Профиль💼')

help_button = types.KeyboardButton('Тех.Поддержка🌎')

games_button = types.KeyboardButton('Игры🎮')

settings_button = types.KeyboardButton('Настройки🔧')




main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(games_button)

main_keyboard.add(profile_button,settings_button)

main_keyboard.add(help_button)

crash_button = types.KeyboardButton('Crash📉')

coin_button = types.KeyboardButton('Монетка🎲')

casino_button = types.KeyboardButton('Рулетка💈')

back_button = types.KeyboardButton('Назад◀️')

games_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    crash_button,coin_button,casino_button
)

games_keyboard.row(back_button) 

addbalance_button = types.KeyboardButton('Изменить баланс')

mode_button = types.KeyboardButton('Изменить статус')

delete_button = types.KeyboardButton('Удалить мамонта')

worker_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(addbalance_button).add(mode_button).add(delete_button).row(back_button)

payment = types.KeyboardButton('Пополнить баланс💰')

get_money = types.KeyboardButton('Вывести💸')

profile_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(payment,get_money)

profile_keyboard.row(back_button)

welcome_keyboard = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('Принять соглашение✅', callback_data='access_sog'))


class payment(StatesGroup):
    summ = State()


class payment_card(StatesGroup):
    summ = State()

class crash(StatesGroup):
    summ = State()
    crash_coefficient = State()

class coin(StatesGroup):
    summ = State()
    choice = State()

class mode(StatesGroup):
    telegram_id = State()
    mode_id = State()


class roulette(StatesGroup):
    summ = State()
    choice = State()

class change_balance(StatesGroup):
    telegram_id = State()
    amount = State()

class deletefrom_user(StatesGroup):
    user_id = State()
    
    
class get_money(StatesGroup):
    money = State()
    payment_choice = State()
    payment_info = State()



def new_user(telegram_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = f"""SELECT * from users WHERE telegram_id={telegram_id}"""
    cursor.execute(query)
    check = cursor.fetchall()
    if check:
        pass
    else:
        cursor.execute("""INSERT INTO users
                    VALUES (?,?,?,?,?,?,?,?)""",(telegram_id, "ru", 1, "1", 0, 0, 1, 0)
        )
        conn.commit()
        return 'new user'


def get_balance(telegram_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT telegram_id,balance FROM users"):
        user_id = row[0]
        if user_id == telegram_id:
            balance = row[1]
            return balance


def new_payment(telegram_id,comment,payment_sum):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(f'UPDATE users SET comment = ? WHERE telegram_id = ?;', (comment, telegram_id))
    cursor.execute(f'UPDATE users SET payment_sum = ? WHERE telegram_id = ?;', (payment_sum, telegram_id))
    conn.commit()

def get_data(telegram_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT telegram_id,comment,payment_sum FROM users"):
        user_id = row[0]
        if user_id == telegram_id:
            comment = row[1]
            amount = row[2]
            return comment, amount
        
        
def get_promo(telegram_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT telegram_id,promo FROM users"):
        user_id = row[0]
        if user_id == telegram_id:
            promo = row[1]
            return promo
    
        
def add_promo(telegram_id, promo):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT telegram_id,promo FROM users"):
        user_id = row[0]
        if int(user_id) == int(telegram_id):
            user_promo = row[1]
            if int(user_promo) == 1 and telegram_id != promo:
                cursor.execute(f'UPDATE users SET promo = ? WHERE telegram_id = ?;', (promo, telegram_id))
                conn.commit()
                return 'good'
            else:
                return 'error'


def add_balance(telegram_id, amount):    
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT telegram_id,balance FROM users"):
        user_id = row[0]
        if int(user_id) == int(telegram_id):
            balance = row[1]
            addbalance = int(balance) + int(amount)
            cursor.execute(f'UPDATE users SET balance = ? WHERE telegram_id = ?;', (addbalance, telegram_id))
            conn.commit()



def pick_money(telegram_id, amount):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT telegram_id,balance FROM users"):
        user_id = row[0]
        if user_id == int(telegram_id):
            balance = row[1]
            addbalance = int(balance) - int(amount)
            cursor.execute(f'UPDATE users SET balance = ? WHERE telegram_id = ?;', (addbalance, telegram_id))
            conn.commit()


def regenerate_code(telegram_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    code = str(random.randint(1000, 10000)) + str(random.choices('qwertyuiop[asdfghjkl', k=8))
    cursor.execute(f'UPDATE users SET comment = ? WHERE telegram_id = ?;', (code, telegram_id))
    conn.commit()


def get_modeuser(telegram_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT telegram_id,mode FROM users"):
        user_id = row[0]
        if user_id == telegram_id:
            mode = row[1]
            return mode

def addmoney_referals(telegram_id, amount):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT telegram_id,promo FROM users"):
        user_id = row[0]
        if user_id == telegram_id:
            user_promo = row[1]
            if int(user_promo) != 1 and int(telegram_id) != int(user_promo):
                return user_promo
            else:
                return 'not ref'


def set_mode(telegram_id, mode):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(f'UPDATE users SET mode = ? WHERE telegram_id = ?;', (mode, telegram_id))
    conn.commit()


def get_referals(telegram_id, promo):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    referals = 0
    for row in cursor.execute("SELECT telegram_id,promo FROM users"):
        ref_promo = row[1]
        if ref_promo == promo:
            referals += 1
    if referals != None:
        return referals
    elif referals == None:
        return 0


            
            
def change_currency(telegram_id, currency):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(f'UPDATE users SET currency = ? WHERE telegram_id = ?;', (currency, telegram_id))
    conn.commit()

def get_currency(telegram_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT telegram_id,currency FROM users"):
        user_id = row[0]
        if user_id == telegram_id:
            currency = row[1]
            return currency

def change_balance_user(telegram_id, amount):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT telegram_id,balance FROM users"):
        user_id = row[0]
        if int(user_id) == int(telegram_id):
            balance = row[1]
            cursor.execute(f'UPDATE users SET balance = ? WHERE telegram_id = ?;', (amount, telegram_id))
            conn.commit()


def new_worker(telegram_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(f'UPDATE users SET worker = ? WHERE telegram_id = ?;', (1, telegram_id))
    conn.commit()

def isworker(telegram_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT telegram_id,worker FROM users"):
        user_id = row[0]
        if int(user_id) == int(telegram_id):
            worker = row[1]
            return worker



@dp.message_handler(commands=['start'])
async def start_func(message: types.Message):
    ref_code = (message.text[7:])
    if ref_code != '':
        check = new_user(message.chat.id)
        if check == 'new user':
            await bot.send_message(message.chat.id, start_message.format(message.from_user.first_name), reply_markup=welcome_keyboard)
            add_promo(message.chat.id, ref_code)
        else:
            balance = get_balance(message.chat.id)
            online = random.randint(400, 460)
            currency = get_currency(message.chat.id)
            if currency == 'ru':
                await bot.send_message(message.chat.id, f'📌 Личный кабинет\n\n💵 Ваш баланс 💵 {balance} р\n💎 Ваши рефералы: {get_referals(message.chat.id, message.chat.id)}\n🎁 Реферальная ссылка:\nhttp://t.me/favoritbet_bot?start={message.chat.id}\n\nПользователей в сети: {online}', reply_markup=profile_keyboard)
            elif currency == 'ua':
                await bot.send_message(message.chat.id, f'📌 Личный кабинет\n\n💵 Ваш баланс 💵 {balance} Грн\n💎 Ваши рефералы: {get_referals(message.chat.id, message.chat.id)}\n🎁 Реферальная ссылка:\nhttp://t.me/favoritbet_bot?start={message.chat.id}\n\nПользователей в сети: {online}', reply_markup=profile_keyboard)     
    else:
        check = new_user(message.chat.id)
        if check == 'new user':
            await bot.send_message(message.chat.id, start_message.format(message.from_user.first_name), reply_markup=welcome_keyboard)
        else:
            balance = get_balance(message.chat.id)
            online = random.randint(400, 460)
            currency = get_currency(message.chat.id)
            if currency == 'ru':
                await bot.send_message(message.chat.id, f'📌 Личный кабинет\n\n💵 Ваш баланс 💵 {balance} р\n💎 Ваши рефералы: {get_referals(message.chat.id, message.chat.id)}\n🎁 Реферальная ссылка:\nhttp://t.me/favoritbet_bot?start={message.chat.id}\n\nПользователей в сети: {online}', reply_markup=profile_keyboard)
            elif currency == 'ua':
                await bot.send_message(message.chat.id, f'📌 Личный кабинет\n\n💵 Ваш баланс 💵 {balance} Грн\n💎 Ваши рефералы: {get_referals(message.chat.id, message.chat.id)}\n🎁 Реферальная ссылка:\nhttp://t.me/favoritbet_bot?start={message.chat.id}\n\nПользователей в сети: {online}', reply_markup=profile_keyboard)


@dp.callback_query_handler(text='access_sog')
async def next_choice(query: types.CallbackQuery):
    message_id = query.message.message_id
    await bot.delete_message(query.message.chat.id,  message_id)
    currency_ru = types.KeyboardButton('RUB🇷🇺')
    currency_ua = types.KeyboardButton('UAH🇺🇦')
    currenct_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row(currency_ru).row(currency_ua)
    await bot.send_message(query.message.chat.id, 'Выберите валюту💶', reply_markup=currenct_keyboard)

@dp.message_handler(text='Тех.Поддержка🌎')
async def help_func(message: types.Message):
    await bot.send_message(message.chat.id, help_message, reply_markup=main_keyboard)

@dp.message_handler(text='Профиль💼')
async def balance_user(message: types.Message):
    balance = get_balance(message.chat.id)
    online = random.randint(400, 460)
    currency = get_currency(message.chat.id)
    if currency == 'ru':
        await bot.send_message(message.chat.id, f'📌 Личный кабинет\n\n💵 Ваш баланс 💵 {balance} р\n💎 Ваши рефералы: {get_referals(message.chat.id, message.chat.id)}\n🎁 Реферальная ссылка:\nhttp://t.me/favoritbet_bot?start={message.chat.id}\n\nПользователей в сети: {online}', reply_markup=profile_keyboard)
    elif currency == 'ua':
        await bot.send_message(message.chat.id, f'📌 Личный кабинет\n\n💵 Ваш баланс 💵 {balance} Грн\n💎 Ваши рефералы: {get_referals(message.chat.id, message.chat.id)}\n🎁 Реферальная ссылка:\nhttp://t.me/favoritbet_bot?start={message.chat.id}\n\nПользователей в сети: {online}', reply_markup=profile_keyboard)



@dp.message_handler(text='Настройки🔧')
async def settings_func(message: types.Message):
    back_button = types.KeyboardButton('Назад◀️')
    currecy_button = types.KeyboardButton('💵Сменить валюту💶')
    settings_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(currecy_button)
    settings_keyboard.add(back_button)
    await bot.send_message(message.chat.id, 'Вы можете поменять валюту', reply_markup=settings_keyboard)


@dp.message_handler(text='💵Сменить валюту💶')
async def change_currency_func(message: types.Message):
    currency_ru = types.KeyboardButton('RUB🇷🇺')
    currency_ua = types.KeyboardButton('UAH🇺🇦')
    currenct_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row(currency_ru).row(currency_ua)
    await bot.send_message(message.chat.id, '🔙 Выберите валюту', reply_markup=currenct_keyboard)


@dp.message_handler(text='Вывести💸', state="*")
async def get_money_func(message: types.Message):
    await bot.send_message(message.chat.id, 'Введите сумму вывода.')
    await get_money.money.set()

@dp.message_handler(state=get_money.money, content_types=types.ContentTypes.TEXT)
async def get_amount_money(message: types.Message, state: FSMContext):
    await state.update_data(money=message.text)
    await bot.send_message(message.chat.id, 'Выберите систему вывода из предложеных!\n\n1)Банковская карта\n2)QIWI кошелек\nДля выбора отправьте цифру, под которой указана нужная Вам система.')
    await get_money.payment_info.set()


@dp.message_handler(state=get_money.payment_info, content_types=types.ContentTypes.TEXT)
async def get_payment_choice(message: types.Message, state: FSMContext):
    await state.update_data(payment_choice=message.text)
    payment = await state.get_data()
    if payment['payment_choice'] != '':
        balance = get_balance(message.chat.id)
        money = payment['money']
        if int(money) <= int(balance):
            await bot.send_message(message.chat.id, f'⚠️Вывод возможен только на реквизиты, с которых пополнялся Ваш баланс в последний раз!⚠️\nВаша заявка на вывод была успешно создана!\nОжидайте!', reply_markup=main_keyboard)
            pick_money(message.chat.id, money)
            await state.finish()
        elif int(money) > int(balance):
            await bot.send_message(message.chat.id, f'У вас не хватает денег⚠️', reply_markup=main_keyboard)
            await state.finish()    
    
    

@dp.message_handler(text='RUB🇷🇺')
async def chance_curencyru(message: types.Message):
    await bot.send_message(message.chat.id, 'Ваша основная валюта: RUB', reply_markup=main_keyboard)
    change_currency(message.chat.id, 'ru')


@dp.message_handler(text='UAH🇺🇦')
async def change_curencyua(message: types.Message):
    await bot.send_message(message.chat.id, 'Ваша основная валюта: UAH', reply_markup=main_keyboard)
    change_currency(message.chat.id, 'ua')


@dp.message_handler(text='Пополнить баланс💰', state="*")
async def payment_balance(message: types.Message):
    currency = get_currency(message.chat.id)
    if currency == 'ru':
        qiwi_button = types.KeyboardButton('Qiwi')
        card = types.KeyboardButton('Карта')
        payments_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(qiwi_button).add(card)
        await bot.send_message(message.chat.id, 'Выберите способ оплаты', reply_markup=payments_keyboard)
    elif currency == 'ua':
        await bot.send_message(message.chat.id, 'Введите сумму на которую вы хотите пополнить баланс\nПример: 100, 200, 500, 1000\nМаксимальная сумма пополнения 15000', reply_markup=main_keyboard)
        await payment.summ.set()


@dp.message_handler(text='Qiwi', state="*")
async def qiwi_payment(message: types.Message):
    await bot.send_message(message.chat.id, 'Введите сумму на которую вы хотите пополнить баланс\nПример: 100, 200, 500, 1000\nМаксимальная сумма пополнения 15000', reply_markup=main_keyboard)
    await payment.summ.set()



@dp.message_handler(text='Карта', state="*")
async def card_payment(message: types.Message):
    await bot.send_message(message.chat.id, 'Введите сумму на которую вы хотите пополнить баланс\nПример: 100, 200, 500, 1000\nМаксимальная сумма пополнения 15000', reply_markup=main_keyboard)
    await payment_card.summ.set()



@dp.message_handler(state=payment_card.summ, content_types=types.ContentTypes.TEXT)
async def payment_card_ru(message: types.Message, state: FSMContext):
    try:
        int(message.text)
        await state.update_data(summ=message.text)
        await bot.send_message(message.chat.id, f'♻️Оплата на банковскую карту\n\nПереведите введенную сумму на карту {card}\n\nВАЖНО!Обязательно укажите комментарий: {message.chat.id}\nЕсли вы не укажите комментарий, деньги не поступят на счёт!\n\nЕсли возникнут проблемы, обратитесь в тех.поддержку')
        await state.finish()
    except ValueError:
        await bot.send_message(message.chat.id, 'Вы ввели не число!')
        await state.finish()
           

@dp.message_handler(state=payment.summ, content_types=types.ContentTypes.TEXT)
async def get_sum(message: types.Message, state: FSMContext):
    currency = get_currency(message.chat.id)
    if currency == 'ru':
        try:
            int(message.text)
            await state.update_data(summ=message.text)
            try:
                inviter = get_promo(message.chat.id)
                first_name = message['from_user']['first_name']
                username = message['from_user']['username']
                await bot.send_message(inviter, f'Попытка пополнения {message.text}руб\nМамонт {first_name}|@{username}')
            except:
                pass
            payment = await state.get_data()
            comment = ''.join(random.choices('qwertyuiopsdfghjkl;zxcvbnm',k=10)) + str(random.randint(1, 1000))
            s = requests.Session()
            s.headers['authorization'] = 'Bearer' + token
            amount = payment['summ']
            parameters = {'publicKey':publick_key,'amount':amount,'phone':phone,'comment':comment}
            h = s.get('https://oplata.qiwi.com/create', params = parameters)
            payment_button = types.InlineKeyboardButton('Оплатить💳', url=h.url)
            keyboard_pay = types.InlineKeyboardMarkup().add(payment_button)
            await bot.send_message(message.chat.id, 'Для оплаты нажмите на кнопку ниже.', reply_markup=keyboard_pay)
            await state.finish()
            new_payment(message.chat.id, comment, amount) 
        except ValueError:
            await bot.send_message(message.chat.id, 'Вы ввели не число!')
            await state.finish()
    elif currency == 'ua': 
        try:
            int(message.text)
            await state.update_data(summ=message.text)
            try:
                inviter = get_promo(message.chat.id)
                first_name = message['from_user']['first_name']
                user_name = message['from_user']['username']
                await bot.send_message(inviter, f'Попытка пополнения {message.text}руб\nМамонт {first_name}|@{username}')
            except:
                pass
            payment = await state.get_data()
            amount = payment['summ']
            await bot.send_message(message.chat.id, f'♻️Оплата на банковскую карту\n\nПереведите введенную сумму на карту {cardua}\n\nВАЖНО!Обязательно укажите комментарий: {message.chat.id}\nЕсли вы не укажите комментарий, деньги не поступят на счёт!\n\nЕсли возникнут проблемы, обратитесь в тех.поддержку')
            await state.finish()
        except ValueError:
            await bot.send_message(message.chat.id, 'Вы ввели не число!')
            await state.finish()



@dp.message_handler(text='Игры🎮')
async def games_func(message: types.Message):
    await bot.send_message(message.chat.id, 'Выберите игру', reply_markup=games_keyboard)

@dp.message_handler(text='Crash📉', state="*")
async def crash_func(message: types.Message):
    await bot.send_message(message.chat.id, 'Введите сумму ставки', reply_markup=main_keyboard)
    await crash.summ.set()

@dp.message_handler(text='Монетка🎲', state='*')
async def coin_game(message: types.Message):
    await bot.send_message(message.chat.id, 'Введите сумму ставки', reply_markup=main_keyboard)
    await coin.summ.set()

@dp.message_handler(text='Рулетка💈', state='*')
async def roulette_game(message: types.Message):
    await bot.send_message(message.chat.id, 'Введите сумму ставки', reply_markup=main_keyboard)
    await roulette.summ.set()

@dp.message_handler(state=roulette.summ, content_types=types.ContentTypes.TEXT)
async def get_summ_roulette(message: types.Message, state: FSMContext):
    choice_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton('= 50'),types.KeyboardButton('> 50'),types.KeyboardButton('< 50'))
    await state.update_data(summ=message.text)
    await bot.send_message(message.chat.id, 'Сейчас выпадет рандомное число от 1 до 99\nВыберите исход события\n\n1.< 50 - 2x\n2.= 50 - x10\n3.> 50 - 2x', reply_markup=choice_keyboard)
    await roulette.choice.set()



@dp.message_handler(state=roulette.choice, content_types=types.ContentTypes.TEXT)
async def get_choice_roulette(message: types.Message, state: FSMContext):
    await state.update_data(choice=message.text)
    info = await state.get_data()
    money = info['summ']
    choice = info['choice']
    if choice == "1":
        win_sum = int(money) * 2
        choice = random.randint(1, 49)
    elif choice == "2":
        win_sum = int(money) * 10
        choice = '50'
    elif choice == "3":
        win_sum = int(money) * 2
        choice = random.randint(51, 99)
    balance = get_balance(message.chat.id)
    await state.finish()
    try:
        if int(money) <= balance:
            mode = get_modeuser(message.chat.id)
            if mode:
                await bot.send_message(message.chat.id, f'Выпало {choice}\nВы выиграли {win_sum}🎉', reply_markup=main_keyboard)
                add_balance(message.chat.id, win_sum)
            elif mode == 2:
                await bot.send_message(message.chat.id, f'Вы проиграли {money}😩', reply_markup=main_keyboard)
                pick_money(message.chat.id, money)
            elif mode == 0:
                coff = random.randint(2, 5)
                if coff == 2:
                    await bot.send_message(message.chat.id, f'Выпало {choice}\nВы выиграли {win_sum}🎉', reply_markup=main_keyboard)
                    add_balance(message.chat.id, win_sum)
                if coff != 2:
                    await bot.send_message(message.chat.id, f'Вы проиграли {money}😩', reply_markup=main_keyboard)
                    pick_money(message.chat.id, money)
        elif int(money) > balance:
            await bot.send_message(message.chat.id, 'Не достаточно денег!', reply_markup=main_keyboard)
    except ValueError:
        await bot.send_message(message.chat.id, 'Вы ввели не число', reply_markup=main_keyboard)  
    
        


@dp.message_handler(state=coin.summ, content_types=types.ContentTypes.TEXT)
async def get_money_coin(message: types.Message, state: FSMContext):
    await state.update_data(summ=message.text)
    await bot.send_message(message.chat.id, 'На что ставите?\n1 - решка\n2 - орёл')
    await coin.choice.set()

@dp.message_handler(state=coin.choice, content_types=types.ContentTypes.TEXT)
async def get_choice_coin(message: types.Message,  state: FSMContext):
    await state.update_data(choice=message.text)
    info = await state.get_data()
    money = info['summ']
    balance = get_balance(message.chat.id)
    await state.finish()
    try:
        if int(money) <= balance:
            mode = get_modeuser(message.chat.id)
            win_sum = int(money) * 2
            if mode: #только выигрыш
                await bot.send_message(message.chat.id, f'Вы выиграли {win_sum}🎉', reply_markup=main_keyboard)
                add_balance(message.chat.id, win_sum)
            elif mode == 2: #только проигрыш
                await bot.send_message(message.chat.id, f'Вы проиграли {money}😩', reply_markup=main_keyboard)
                pick_money(message.chat.id, money)
            elif mode == 0: #рандом
                win = random.randint(1, 2)
                if win:
                    await bot.send_message(message.chat.id, f'Вы проиграли {money}😩', reply_markup=main_keyboard)
                    pick_money(message.chat.id, money)
                elif win == 2:
                    await bot.send_message(message.chat.id, f'Вы выиграли {win_sum}🎉', reply_markup=main_keyboard)
                    add_balance(message.chat.id, win_sum)
        else:
            await bot.send_message(message.chat.id, 'Вам не хватает денег!', reply_markup=main_keyboard) 
    except ValueError:
        await bot.send_message(message.chat.id, 'Вы ввели не число', reply_markup=main_keyboard)  
    
    
@dp.message_handler(text='Назад◀️')
async def back_menu(message: types.Message):
    await bot.send_message(message.chat.id, 'Вернул вас в главное меню📚', reply_markup=main_keyboard)



@dp.message_handler(state=crash.summ, content_types=types.ContentTypes.TEXT)
async def get_sum(message: types.Message, state: FSMContext):
    await state.update_data(summ=message.text)
    await bot.send_message(message.chat.id, 'Введите возможный коэффицент crash.')
    await crash.crash_coefficient.set()


@dp.message_handler(state=crash.crash_coefficient, content_types=types.ContentTypes.TEXT)
async def generate_win(message: types.Message,  state: FSMContext):
    await state.update_data(crash_coefficient=message.text)
    info = await state.get_data()
    money = info['summ']
    balance = get_balance(message.chat.id)
    try:
        if int(money) <= balance:
            coefficient = info['crash_coefficient']
            win_sum = int(money) * int(coefficient)
            await state.finish()
            await bot.send_message(message.chat.id, f'Ваша ставка {money} 💸\nКоэффициент {coefficient}📈\nВозможный выйгрыш {win_sum} 📊', reply_markup=main_keyboard)
            mode = get_modeuser(message.chat.id)
            if mode: #только выигрыш
                await bot.send_message(message.chat.id, f'Вы выиграли {win_sum}🎉', reply_markup=main_keyboard)
                add_balance(message.chat.id, win_sum)
            elif mode == 2: #только проигрыш
                await bot.send_message(message.chat.id, f'Вы проиграли {money}😩', reply_markup=main_keyboard)
                pick_money(message.chat.id, money)
            elif mode == 0: #рандом
                win = random.randint(1, 2)
                if win:
                    await bot.send_message(message.chat.id, f'Вы проиграли {money}😩', reply_markup=main_keyboard)
                    pick_money(message.chat.id, money)
                elif win == 2:
                    await bot.send_message(message.chat.id, f'Вы выиграли {win_sum}🎉', reply_markup=main_keyboard)
                    add_balance(message.chat.id, win_sum)
        
        else:
            await bot.send_message(message.chat.id, 'У вас не хватает денег!', reply_markup=main_keyboard)
            await state.finish()
    except ValueError:  
        await bot.send_message(message.chat.id, 'Вы ввели не число', reply_markup=main_keyboard)     



    
@dp.message_handler(text='Воркер')
async def menu_worker(message: types.Message):
    check = isworker(message.chat.id)
    if check:
        await bot.send_message(message.chat.id, 'Вы вошли в воркер панель!', reply_markup=worker_keyboard)
    else:
        await bot.send_message(message.chat.id, 'Используйте кнопки для управления ботом.', reply_markup=main_keyboard)


@dp.message_handler(text='Изменить баланс', state="*")
async def add_balance_user(message: types.Message, state: FSMContext):
    ref_list = []
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT telegram_id,promo FROM users"):
        promo = row[1]
        if promo == message.chat.id:
            telegram_id = row[0]
            first_name = message['from_user']['first_name']
            last_name = message['from_user']['last_name']
            username = message['from_user']['username']
            ref_list.append(f'\n({telegram_id},{first_name}|{last_name}|{username},{get_balance(telegram_id)},{get_modeuser(telegram_id)})')
    ids = '\n'.join(ref_list)
    try:
        await bot.send_message(message.chat.id, f'{ids}', reply_markup=worker_keyboard)
        await bot.send_message(message.chat.id, 'Введите ID пользователя', reply_markup=worker_keyboard)
        await change_balance.telegram_id.set()
    except:

        await bot.send_message(message.chat.id, 'У вас нет рефералов!', reply_markup=worker_keyboard)


@dp.message_handler(state=change_balance.telegram_id, content_types=types.ContentTypes.TEXT)
async def get_telegram_id(message: types.Message, state: FSMContext):
    await state.update_data(telegram_id=message.text)
    await bot.send_message(message.chat.id, 'Введите баланс который нужно поставить пользователю.', reply_markup=worker_keyboard)
    await change_balance.amount.set()


@dp.message_handler(state=change_balance.amount, content_types=types.ContentTypes.TEXT)
async def get_amount_balance(message: types.Message, state: FSMContext):
    await state.update_data(amount=message.text)
    try:
        info = await state.get_data()
        telegram_id = info['telegram_id']
        amount = info['amount']
        int(amount)
        change_balance_user(telegram_id, amount)
        await state.finish()
        await bot.send_message(message.chat.id, f'Сумма {amount} добавлена', reply_markup=worker_keyboard)
    except ValueError:
        await bot.send_message(message.chat.id, 'Вы ввели не число')
        await state.finish()

@dp.message_handler(text='Изменить статус', state="*")
async def chance_mode(message: types.Message, state: FSMContext):
    ref_list = []
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT telegram_id,promo FROM users"):
        promo = row[1]
        if promo == message.chat.id:
            telegram_id = row[0]
            first_name = message['from_user']['first_name']
            last_name = message['from_user']['last_name']
            username = message['from_user']['username']
            ref_list.append(f'\n({telegram_id},{first_name}|{last_name}|{username},{get_balance(telegram_id)},{get_modeuser(telegram_id)})')
    ids = '\n'.join(ref_list)
    try:
        await bot.send_message(message.chat.id, f'{ids}', reply_markup=worker_keyboard)
        await bot.send_message(message.chat.id, 'Введите ID пользователя которому нужно сменить режим игры.', reply_markup=worker_keyboard)
        await mode.telegram_id.set()
    except:
        await bot.send_message(message.chat.id, 'У вас нет рефералов!', reply_markup=worker_keyboard)
        await state.finish()

@dp.message_handler(state=mode.telegram_id, content_types=types.ContentTypes.TEXT)
async def get_telegram_id(message: types.Message, state: FSMContext):
    await state.update_data(telegram_id=message.text)
    await bot.send_message(message.chat.id, 'Введите режим игры\n1 - выигрыш\n2 - проигрыш\n0 - рандом', reply_markup=worker_keyboard)
    await mode.mode_id.set()

@dp.message_handler(state=mode.mode_id, content_types=types.ContentTypes.TEXT)
async def get_mode(message: types.Message, state: FSMContext):
    try:
        await state.update_data(mode_id=message.text)
        info = await state.get_data()
        telegram_id = info['telegram_id']
        mode = info['mode_id']
        int(message.text)
        await bot.send_message(message.chat.id, f'Для пользователя {telegram_id} установлен режим игры {mode}')
        set_mode(telegram_id, mode)
        await state.finish()
    except ValueError:
        await bot.send_message(message.chat.id, 'Вы ввели не число!', reply_markup=worker_keyboard)

@dp.message_handler(text='Удалить мамонта', state="*")
async def delete_user(message: types.Message):
    ref_list = []
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT telegram_id,promo FROM users"):
        promo = row[1]
        if promo == message.chat.id:
            telegram_id = row[0]
            first_name = message['from_user']['first_name']
            last_name = message['from_user']['last_name']
            username = message['from_user']['username']
            ref_list.append(f'\n({telegram_id},{first_name}|{last_name}|{username},{get_balance(telegram_id)},{get_modeuser(telegram_id)})')
    ids = '\n'.join(ref_list)
    try:
        await bot.send_message(message.chat.id, f'{ids}', reply_markup=worker_keyboard)
        await bot.send_message(message.chat.id, 'Введите ID мамонта которого хотите удалить', reply_markup=worker_keyboard)
        await change_balance.telegram_id.set()
    except:
        await bot.send_message(message.chat.id, 'У вас нет рефералов!', reply_markup=worker_keyboard)


@dp.message_handler(state=deletefrom_user.user_id, content_types=types.ContentTypes.TEXT)
async def get_telegramid_user(message: types.Message, state: FSMContext):
    await state.update_data(user_id=message.text)
    info = await state.get_data()
    telegram_id = info['user_id']
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT telegram_id,promo FROM users"):
        user_id = row[0]
        if int(user_id) == int(telegram_id):
            user_promo = row[1]
            cursor.execute(f'UPDATE users SET promo = ? WHERE telegram_id = ?;', (1, telegram_id))
            conn.commit()
    await bot.send_message(message.chat.id, 'Мамонт удален!', reply_markup=worker_keyboard)
    await state.finish()


@dp.message_handler()
async def command_handler(message: types.Message):
    if "/worker" in message.text and message.chat.id in admins:
        telegram_id = message.text.replace('/worker', '').replace(' ', '')
        new_worker(telegram_id)




executor.start_polling(dp)


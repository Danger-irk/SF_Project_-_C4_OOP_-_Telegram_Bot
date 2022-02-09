import telebot
from telebot import types

from config import TOKEN, exchanges
from extensions import Convertor, Rate, APIException

bot = telebot.TeleBot(TOKEN)

markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
buttons = []
for key, value in exchanges.items():
    buttons.append(types.KeyboardButton(f"{value} - {key}"))
markup.add(*buttons)


# start / help
@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = """Приветствую, %s %s!

Данный бот умеет конвертировать валюты.

Для конвертации валют отправьте команду /convert

Для получения курса - /rate
"""
    bot.send_message(message.chat.id, text % (message.chat.first_name, message.chat.last_name))


# convert
@bot.message_handler(commands=['convert'])
def converter(message: telebot.types.Message):
    text = 'Выберите валюту из коророй конвертировать:'
    bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(message, base_handler)


def base_handler(message: telebot.types.Message):
    base = message.text.split()[-1].strip().upper()
    text = 'Выберите валюту в корорую конвертировать:'
    bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(message, symbol_handler, base)


def symbol_handler(message: telebot.types.Message, base):
    symbol = message.text.split()[-1].strip().upper()
    text = 'Выберите количество валюты для конвертиртации:'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, symbol)


def amount_handler(message: telebot.types.Message, base, symbol):
    amount = message.text.upper().strip()
    try:
        new_price = Convertor.get_price(base, symbol, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f"Ошбка конвертации: \n{e}")
    else:
        text = f"Цена {amount} {exchanges.get(base)} в {exchanges.get(symbol)} : {new_price}\n" \
               f"/convert \t /rate \t /help"
        bot.send_message(message.chat.id, text)


@bot.message_handler(commands="rate")
def rate(message: telebot.types.Message):
    text = 'Выберите валюту:'
    bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(message, rate_handler)


def rate_handler(message: telebot.types.Message):
    name_rate = message.text.split()[-1].strip().upper()
    try:
        new_rate = Rate.get_rate(name_rate)
    except APIException as e:
        bot.send_message(message.chat.id, f"Ошбка: \n{e}")
    else:
        text = f"Курс {exchanges.get(name_rate)} составляет - {new_rate} рублей.\n" \
               f"/rate \t /convert \t /help"
        bot.send_message(message.chat.id, text)


bot.polling(non_stop=True)

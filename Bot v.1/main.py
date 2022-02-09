import telebot

from config import TOKEN, exchanges
from extensions import Convertor, APIException


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = """Приветствую, %s %s!

Данный бот умеет конвертировать валюты.

Чтобы получить перечень валют отправьте команду /values.

Для конвертации валют введите обозначение первой и второй валюты, а так же нужное количество.

Например:
USD RUB 100
"""
    bot.send_message(message.chat.id, text % (message.chat.first_name, message.chat.last_name))


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key, value in exchanges.items():
        text = ''.join((text, '\n', key, "\t - \t", value))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    try:
        base, symbols, amount = message.text.upper().split()
    except ValueError:
        bot.reply_to(message, "Неверное количество параметров.")
        return

    try:
        new_price = Convertor.get_price(base, symbols, amount)
        bot.reply_to(message, f"Цена {amount} {exchanges.get(base)} в {exchanges.get(symbols)} : {new_price}")
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде: \n{e}")


bot.polling()

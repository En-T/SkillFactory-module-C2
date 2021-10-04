import telebot
import json
import requests
from config import TOKEN, exchanger
from extensions import Converter, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands= ['start', 'help'])
def start(message: telebot.types.Message):
    text = '''/values - список доступных валют,
валюта1 валюта2 сумма - переводит из валюты1 в валюту2'''
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands= ['values'])
def valuel(message: telebot.types.Message):
    text = "Доступные валюты:\n"
    text += '\n'.join(exchanger.keys())
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(" ")
    values = list(map(str.lower, values))
    try:
        total = Converter.get_price(values)
    except APIException as e:
        bot.reply_to(message, e)
    except Exception as e:
        bot.reply_to(message, e)
    else:
        bot.send_message(message.chat.id, f"Цена {values[2]} {exchanger[values[0]]} = {total} {exchanger[values[1]]}")

bot.polling(non_stop=True, interval=0)
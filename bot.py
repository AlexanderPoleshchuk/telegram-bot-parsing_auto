import telebot
from parsing import *

TOKEN = '1235757002:AAHDvXHqG5wohEsEAJPzPv8Y3hpWbljxqgQ'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет!\nВставь ссылку с интересующей тебя марки или '
                                      'модели автомобиля сайта https://autoby.by/,'
                                      ' а я подберу для тебя варианты.')


@bot.message_handler(content_types=['text'])
def send_text(message):
    try:
        parse(message.text)
        doc = open('../telegram-bot-parsing_auto/cars.csv')
        bot.send_document(message.chat.id, doc)
    except requests.exceptions.MissingSchema:
        bot.send_message(message.chat.id, 'Неправильная ссылка')

bot.polling()

import telebot
# с помощью типов можно создавать клавиатуры
from telebot import types
# импорт из файла functions
from functions import marks_buttons, model_buttons, search_models, zayavka_done, clients_base, rasylka_message

token = '5380562272:AAFqodiUpENCtx7oD8f5xnbIDNOoxJW6YMY'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    sent = bot.send_message('1338281106', 'Выберите базу для рассылки')
    bot.register_next_step_handler(sent, post_perehvat_2)


def post_perehvat_2(message):
    bot.copy_message('127154290', '1338281106', message.id)


bot.polling()
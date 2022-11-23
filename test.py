import telebot
# с помощью типов можно создавать клавиатуры
from telebot import types
# импорт из файла functions
from functions import marks_buttons, model_buttons, search_models, zayavka_done, clients_base, rasylka_message

token =
bot = telebot.TeleBot(token)

rasylka = None


class rasylka_message:  # класс хранения сообщения для рассылки
    def __init__(self, post):
        self.post = post

    def _get_message_(self):
        return self.post


@bot.message_handler(commands=['sent_message'])  # команда для переброски клиента из базы потенциальных клиентов в
def sent_message(message):    # базу старых клиентов
    if message.chat.id == 1338281106:
        sent = bot.send_message('1338281106', 'Введи id чата клиента, которому нужно написать от лица бота')
        bot.register_next_step_handler(sent, sent_message_perehvat_1)   # перехватывает ответ пользователя на сообщение "sent" и
                                                              # и направляет его аргументом в функцию base_perehvat
    else:
        bot.send_message(message.chat.id, 'У Вас нет прав для использования данной команды')


def sent_message_perehvat_1(message):
    try:
        global rasylka
        rasylka = rasylka_message(message.text)
        sent = bot.send_message('1338281106', 'Введите текст сообщения')
        bot.register_next_step_handler(sent, sent_message_perehvat_2)
    except ValueError:
        bot.send_message('1338281106', 'Неккоректное значение. Воспользуйтесь командой /sent_message еще раз')


def sent_message_perehvat_2(message):
    kb2 = types.ReplyKeyboardRemove()
    global rasylka
    bot.copy_message(rasylka.post, '1338281106', message.id, reply_markup=kb2)


bot.polling()
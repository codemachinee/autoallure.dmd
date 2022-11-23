import telebot
# с помощью типов можно создавать клавиатуры
from telebot import types
# импорт из файла functions
from functions import marks_buttons, model_buttons, search_models, zayavka_done, clients_base, rasylka_message

token = '5380562272:AAFqodiUpENCtx7oD8f5xnbIDNOoxJW6YMY'
bot = telebot.TeleBot(token)

rasylka = None


@bot.message_handler(commands=['start'])
def zayavka_done(message):
    kb2 = types.ReplyKeyboardRemove()
    if message.from_user.username is not None:
        sent = bot.send_message(message.chat.id, f'Заявка оформлена и передана мастеру, с Вами свяжутся в ближайшее время. '
                                          'Спасибо, что выбрали нас.🤝\n'
                                          f'Для нового рассчета воспользуйтесь командой /price', reply_markup=kb2)
        bot.send_message(127154290, f'🚨!!!СРОЧНО!!!🚨\n'
                                       f'Хозяин, поступила ЗАЯВКА от:\n'
                                       f'Псевдоним: @{message.from_user.username}\n'
                                       f'id чата: {message.chat.id}\n'
                                       f'Быстрее согласуй дату и закрой заявку пока он не слился'
                                       f'\n'
                                       f'В случае положительной отработки заявки не забудь перевести клиента из базы '
                                       f'"потенциальные клиенты" в базу "старые клиенты" с помощью команды\n '
                                       f'/next_level_base\n'
                                       f'/sent_message - отправить сообщение с помощью бота')
        bot.register_next_step_handler(sent, perehvat)
    else:
        bot.send_message(message.chat.id, f'Заявка оформлена и передана мастеру, пожалуйста перейдите в чат @pogonin21 '
                                          f'и отправьте любое сообщение или отправьте свой номер '
                                          f'телефона, чтобы с Вами связались. Спасибо, что выбрали нас.🤝\n'
                                          f'Для нового рассчета воспользуйтесь командой /price', reply_markup=kb2)

        bot.send_message('127154290', f'🚨!!!СРОЧНО!!!🚨\n'
                                      f'Хозяин, поступила ЗАЯВКА от:\n'
                                      f'Псевдоним: @{message.from_user.username}\n'
                                      f'id чата: {message.chat.id}\n'
                                      f'Быстрее согласуй дату и закрой заявку пока он не слился'
                                      f'\n'
                                      f'В случае положительной отработки заявки не забудь перевести клиента из базы '
                                      f'"потенциальные клиенты" в базу "старые клиенты" с помощью команды\n '
                                      f'/next_level_base\n'
                                      f'/sent_message - отправить сообщение с помощью бота')


def perehvat(message):
    bot.send_message('127154290', 'Сообщение от клиента:')
    bot.copy_message('127154290', message.chat.id, message.id)


bot.polling()
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile, ReplyKeyboardRemove
from test_functions import *
from passwords import *
admin_account = igor


async def start(message: Message, bot):
    if message.chat.id == admin_account:
        start_file = FSInputFile(r'start_logo.png', 'rb')
        await bot.send_photo(message.chat.id, start_file, caption=f'Здравствуйте! Вас приветствует autoallure.dmd_bot - '
                                                                  f'надежный сервис и помощник по уходу за Вашим '
                                                                  f'автомобилем.﻿🚘\n\n'
                                                                  f'/price - рассчет цены на услуги autoallure для '
                                                                  f'Вашего авто\n/help - все возможности бота\n\n'
                                                                  f'режим: Администратор')

    else:
        start_file = FSInputFile(r'start_logo.png', 'rb')
        await bot.send_photo(message.chat.id, start_file,
                             caption=f'Здравствуйте! Вас приветствует autoallure.dmd_bot - '
                                     f'надежный сервис и помощник по уходу за Вашим '
                                     f'автомобилем .﻿🚘\n\n'
                                     f'/price - рассчет цены на услуги autoallure для '
                                     f'Вашего авто\n/help - все возможности бота\n\n')


async def help(message: Message, bot):
    if message.chat.id == admin_account:      # условия демонстрации различных команд для админа и клиентов
        await bot.send_message(message.chat.id, f'Основные команды поддерживаемые ботом:\n'
                                                     f'/price -  рассчет услуг для любого авто\n'
                                                     f'/start - инициализация бота\n'
                                                     f'/help - справка по боту\n'
                                                     f'/post - устроить рассылку\n'
                                                     f'/next_level_base - перевод клиента из базы "потенциальные клиенты" в базу '
                                                     f'"старые клиенты"\n'
                                                     f'/sent_message -  отправка через бота сообщения клиенту по id чата\n'
                                                     f'/result - посмотреть на отзывы и галерею с результатом работ')
    else:
        await bot.send_message(message.chat.id, f'Основные команды поддерживаемые ботом:\n'
                                                     f'/price -  рассчет услуг для любого авто\n'
                                                     f'/start - инициализация бота\n'
                                                     f'/help - справка по боту\n'
                                                     f'/result - посмотреть на отзывы и галерею с результатом работ')


async def result(message: Message, bot):
    await bot.send_message(message.chat.id, 'перейдите по ссылке: https://drive.google.com/drive/folders/'
                                            '1ZoR3prmxJtCmeW8Ik-rDB0S4FxpzaWPc')


async def price(message: Message, bot):
    await bot.send_message(text=f'Пожалуйста выберите марку Вашего автомобиля 🏎:', chat_id=message.chat.id,
                           reply_markup=kb_price)


async def check_callbacks(callback: CallbackQuery, bot, state: FSMContext):
    if callback.data == 'page_one':
        await Buttons(bot, callback.message).marka_buttons(next_button='page_two', back_button=None)
    elif callback.data == 'page_two':
        await Buttons(bot, callback.message).marka_buttons(next_button=None, back_button='page_one')
    elif callback.data == 'AUDI':
        await Buttons(bot, callback.message).models_buttons(callback.data)
    elif callback.data == 'price_menu':
        await bot.edit_message_text(chat_id=callback.message.chat.id, text=f'Пожалуйста выберите марку Вашего '
                                                                           f'автомобиля 🚐:',
                                    message_id=callback.message.message_id, reply_markup=kb_price)


async def check_message(message: Message, bot):
    if message.text:
        kb2 = ReplyKeyboardRemove()  # удаление клавиатуры
        await bot.send_message(message.chat.id, '...', reply_markup=kb2)



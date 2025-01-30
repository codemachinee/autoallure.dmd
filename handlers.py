from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile, ReplyKeyboardRemove
from functions import*


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
    marks_buttons(bot, message)


async def check_callbacks(callback: CallbackQuery, bot, state: FSMContext):
    pass


async def check_message(message: Message, bot):
    if message.text:
        kb2 = ReplyKeyboardRemove()  # удаление клавиатуры
        await bot.send_message(message.chat.id, '...', reply_markup=kb2)



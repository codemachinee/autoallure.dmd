from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile, ReplyKeyboardRemove, InputMediaPhoto
from keyboards import *
from passwords import *
from FSM import *
admin_account = igor


async def start(message: Message, bot, state: FSMContext):
    await state.clear()
    if message.chat.id == admin_account:
        start_file = FSInputFile(r'start_logo.png', 'rb')
        await bot.send_photo(message.chat.id, start_file, caption=f'Здравствуйте! Вас приветствует autoallure.dmd_bot - '
                                                                  f'надежный сервис и помощник по уходу за Вашим '
                                                                  f'автомобилем.🚘\n\n'
                                                                  f'/price - рассчет цены на услуги autoallure для '
                                                                  f'Вашего авто\n/help - все возможности бота\n\n'
                                                                  f'режим: Администратор')

    else:
        start_file = FSInputFile(r'start_logo.png', 'rb')
        await bot.send_photo(message.chat.id, start_file,
                             caption=f'Здравствуйте! Вас приветствует autoallure.dmd_bot - '
                                     f'надежный сервис и помощник по уходу за Вашим '
                                     f'автомобилем.🚘\n\n'
                                     f'/price - рассчет цены на услуги autoallure для '
                                     f'Вашего авто\n/help - все возможности бота\n\n')


async def help(message: Message, bot, state: FSMContext):
    await state.clear()
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


async def result(message: Message, bot, state: FSMContext):
    await state.clear()
    await bot.send_message(message.chat.id, 'перейдите по ссылке: https://drive.google.com/drive/folders/'
                                            '1ZoR3prmxJtCmeW8Ik-rDB0S4FxpzaWPc')


async def sent_message(message: Message, bot, state: FSMContext):
    await state.clear()
    if message.chat.id == admin_account:
        await bot.send_message(admin_account, 'Введи id чата клиента, которому нужно написать от лица бота')
        await state.set_state(Message_from_admin.user_id)
    else:
        await bot.send_message(message.chat.id, 'У Вас нет прав для использования данной команды')


async def price(message: Message, bot, state: FSMContext):
    await state.clear()
    await bot.send_message(text=f'Пожалуйста выберите марку Вашего автомобиля 🏎:', chat_id=message.chat.id,
                           reply_markup=kb_price)


async def post(message: Message, bot, state: FSMContext):
    await state.clear()
    if message.chat.id == admin_account:
        await Buttons(bot, message).rasylka_buttons()
        await state.set_state(Rassylka.post)

    else:
        bot.send_message(message.chat.id, 'У Вас нет прав для использования данной команды')


async def check_callbacks(callback: CallbackQuery, bot, state: FSMContext):
    async with aiofiles.open('price.json', "r", encoding="utf-8") as file:
        content = await file.read()
        data = json.loads(content)
        if callback.data == 'page_one':
            await Buttons(bot, callback.message).marka_buttons(next_button='page_two', back_button=None)
        elif callback.data == 'page_two':
            await Buttons(bot, callback.message).marka_buttons(next_button=None, back_button='page_one')
        elif callback.data == 'zayavka_yes':
            if callback.from_user.username is not None:
                await bot.edit_message_text(text=f'Заявка оформлена и передана мастеру, с Вами свяжутся в ближайшее время. '
                                            f'Спасибо, что выбрали нас.🤝\n\n'
                                            f'Если желаете сообщить что-то дополнительно, отправьте в сообщении 💬\n'
                                            f'Для нового рассчета воспользуйтесь командой /price',
                                            chat_id=callback.message.chat.id, message_id=callback.message.message_id)
                await bot.send_message(admin_account, f'🚨!!!СРОЧНО!!!🚨\n'
                                                f'Хозяин, поступила ЗАЯВКА от:\n'
                                                f'Псевдоним: @{callback.from_user.username}\n'
                                                f'id чата: {callback.message.chat.id}\n'
                                                f'Быстрее согласуй дату и закрой заявку пока он не слился'
                                                f'\n'
                                                f'В случае положительной отработки заявки не забудь перевести клиента из базы '
                                                f'"потенциальные клиенты" в базу "старые клиенты" с помощью команды\n '
                                                f'/next_level_base\n'
                                                f'/sent_message - отправить сообщение с помощью бота')
            else:
                await bot.send_message(callback.message.chat.id, f'Заявка оформлена и передана мастеру, пожалуйста перейдите в чат '
                                                  f'@pogonin21 и напишите любое сообщение или отправьте в ответ на это '
                                                  f'сообщение свой номер телефона в любом формате. '
                                                  f'Спасибо, что выбрали нас.🤝\n'
                                                  f'Для нового рассчета воспользуйтесь командой /price')
                await bot.send_message(admin_account, f'🚨!!!СРОЧНО!!!🚨\n'
                                                f'Хозяин, поступила ЗАЯВКА от:\n'
                                                f'Псевдоним: @{callback.from_user.username}\n'
                                                f'id чата: {callback.message.chat.id}\n'
                                                f'Быстрее согласуй дату и закрой заявку пока он не слился\n'
                                                f'В случае положительной отработки заявки не забудь перевести клиента из базы '
                                                f'"потенциальные клиенты" в базу "старые клиенты" с помощью команды\n '
                                                f'/next_level_base\n'
                                                f'/sent_message - отправить сообщение с помощью бота')
            await state.set_state(Another_model.message)
        elif callback.data in list(data.keys()):
            await state.update_data(marka=callback.data)
            await Buttons(bot, callback.message).models_buttons(callback.data)
        elif callback.data == 'price_menu':
            await bot.edit_message_text(chat_id=callback.message.chat.id, text=f'Пожалуйста выберите марку Вашего '
                                                                               f'автомобиля 🚐:',
                                        message_id=callback.message.message_id, reply_markup=kb_price)
        elif callback.data == 'price_menu_two':
            await bot.edit_message_text(chat_id=callback.message.chat.id, text=f'Пожалуйста выберите марку Вашего '
                                                                               f'автомобиля 🚐:',
                                        message_id=callback.message.message_id, reply_markup=kb_price_two)
        elif callback.data.startswith('another_'):
            kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="↩️ Вернуться",
                                                                             callback_data=callback.data[8:])]])
            await state.update_data(marka=callback.data[8:])
            await bot.edit_message_text(chat_id=callback.message.chat.id, text=f'Пожалуйста введите марку Вашего '
                                                                               f'автомобиля ⌨️:',
                                        message_id=callback.message.message_id, reply_markup=kb)
            await state.set_state(Another_model.model)
        elif callback.data.endswith('_class'):
            mes = await bot.edit_message_text(text=f'загрузка..🚀', chat_id=callback.message.chat.id, message_id=callback.message.message_id)
            data = await state.get_data()
            data_marka = data.get('marka')
            file_open = FSInputFile(f'{callback.data}.png', 'rb')
            media = InputMediaPhoto(media=file_open, caption=f'Готово!\n'
                                                             f'Стоимость услуг для Вашего автомобиля {data_marka}\n'
                                                             f'соответствует {callback.data[0]} ценовому классу.\n'
                                                             f'/help - справка по боту \n'
                                                             f'/result - посмотреть на отзывы и результат работ')
            await bot.edit_message_media(media=media, chat_id=callback.message.chat.id, message_id=mes.message_id)
            await Buttons(bot, callback.message).zayavka_buttons(data_marka)
            await bot.send_message(admin_account, f'Хозяин! Замечена активность:\n'
                                                  f'Имя: {callback.from_user.first_name}\n'
                                                  f'Фамилия: {callback.from_user.last_name}\n'
                                                  f'Никнейм: {callback.from_user.username}\n'
                                                  f'Ссылка: @{callback.from_user.username}\n'
                                                  f'Авто: {data_marka} {callback.data[0]} класса')
            await clients_base(bot, callback.message, auto_model=f'{data_marka} {callback.data[0]} класса').chec_and_record()
            await state.clear()
        elif callback.data == 'Общая база клиентов':
            await bot.edit_message_text(text='База для рассылки: Общая база клиентов\nОтправь мне пост 💬',
                                        chat_id=admin_account, message_id=callback.message.message_id)
            await state.update_data(base=callback.data)
            await state.set_state(Rassylka.post)
        elif callback.data == 'База потенциальных клиентов':
            await bot.edit_message_text(text='База для рассылки: ️База потенциальных клиентов\nОтправь мне пост 💬',
                                        chat_id=admin_account, message_id=callback.message.message_id)
            await state.update_data(base=callback.data)
            await state.set_state(Rassylka.post)
        elif callback.data == 'База старых клиентов':
            await bot.edit_message_text(text='База для рассылки: ️База старых клиентов\nОтправь мне пост 💬',
                                        chat_id=admin_account, message_id=callback.message.message_id)
            await state.update_data(base=callback.data)
            await state.set_state(Rassylka.post)


async def check_message(message: Message, bot):
    if message.text:
        kb2 = ReplyKeyboardRemove()  # удаление клавиатуры
        await bot.send_message(message.chat.id, '...', reply_markup=kb2)



# библиотека телеграм-бота
import telebot
# с помощью типов можно создавать клавиатуры
from telebot import types
# библиотека для выполнения фоновых процессов в определенное время
from apscheduler.schedulers.background import BackgroundScheduler
# импорт из файла functions
from functions import marks_buttons, model_buttons, search_models, zayavka_done, clients_base, rasylka_message, admin_account

#token = '5380562272:AAFqodiUpENCtx7oD8f5xnbIDNOoxJW6YMY'
token = '1478162901:AAH6hKsBTTxVg8mEuR0sgTwpiqjf4hbA5WY'
bot = telebot.TeleBot(token)


auto_model = None   # переменная для записи модели авто клиента
rasylka = None   # переменная для переопределения класса в который записывается и хранится сообщение рассылки


@bot.message_handler(commands=['start'])    # перехватчик команды /start
def start(message):
    kb2 = types.ReplyKeyboardRemove()    # удаление клавиатуры
    bot.send_message(message.chat.id, '...', reply_markup=kb2)
    file_open = open("start_logo.png", 'rb')    # открытие и чтение файла стартовой картинки
    bot.send_photo(message.chat.id, file_open, '''Здравствуйте!
Вас приветствует autoallure.dmd_bot - надежный сервис и помощник по уходу за Вашим автомобилем .﻿🚘

/price - рассчет цены на услуги autoallure для Вашего авто
/help - все возможности бота''')


@bot.message_handler(commands=['help'])
def help(message):
    kb2 = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, '...', reply_markup=kb2)
    if message.chat.id == admin_account:      # условия демонстрации различных команд для админа и клиентов
        bot.send_message(message.chat.id, f'Основные команды поддерживаемые ботом:\n'
                                          f'/price -  рассчет услуг для любого авто\n'
                                          f'/start - инициализация бота\n'
                                          f'/help - справка по боту\n'
                                          f'/post - устроить рассылку\n'
                                          f'/next_level_base - перевод клиента из базы "потенциальные клиенты" в базу '
                                          f'"старые клиенты"\n'
                                          f'/sent_message -  отправка через бота сообщения клиенту по id чата'
                                          f'/result - посмотреть на отзывы и галерею с результатом работ')
    else:
        bot.send_message(message.chat.id, f'Основные команды поддерживаемые ботом:\n'
                                          f'/price -  рассчет услуг для любого авто\n'
                                          f'/start - инициализация бота\n'
                                          f'/help - справка по боту\n'
                                          f'/result - посмотреть на отзывы и галерею с результатом работ')


@bot.message_handler(commands=['price'])
def price(message):
    marks_buttons(bot, message)    # класс по формированию различных клавиатур, располагается в functions


@bot.message_handler(commands=['next_level_base'])  # команда для переброски клиента из базы потенциальных клиентов в
def next_level_base(message):                                                        # базу старых клиентов
    if message.chat.id == admin_account:
        sent = bot.send_message(admin_account, 'Введи никнейм клиента без знака @, которого нужно переместить '
                                              'в базу данных "старые клиенты"')
        bot.register_next_step_handler(sent, base_perehvat)   # перехватывает ответ пользователя на сообщение "sent" и
                                                              # и направляет его аргументом в функцию base_perehvat
    else:
        bot.send_message(message.chat.id, 'У Вас нет прав для использования данной команды')


@bot.message_handler(commands=['sent_message'])  # команда для переброски клиента из базы потенциальных клиентов в
def sent_message(message):    # базу старых клиентов
    if message.chat.id == admin_account:
        sent = bot.send_message(admin_account, 'Введи id чата клиента, которому нужно написать от лица бота')
        bot.register_next_step_handler(sent, sent_message_perehvat_1)   # перехватывает ответ пользователя на сообщение "sent" и
                                                              # и направляет его аргументом в функцию base_perehvat
    else:
        bot.send_message(message.chat.id, 'У Вас нет прав для использования данной команды')


@bot.message_handler(commands=['post'])
def post(message):
    if message.chat.id == admin_account:
        sent = bot.send_message(admin_account, 'Введи текст поста и отправь мне..')
        bot.register_next_step_handler(sent, post_perehvat_1)
    else:
        bot.send_message(message.chat.id, 'У Вас нет прав для использования данной команды')


@bot.message_handler(commands=['result'])
def result(message):
    bot.send_message(message.chat.id, 'перейдите по ссылке: https://drive.google.com/drive/folders/1ZoR3prmxJtCmeW8Ik-'
                                      'rDB0S4FxpzaWPc')


@bot.message_handler(func=lambda m: m.text)  # перехватчик текстовых сообщений
def chek_message_auto(m):
    kb2 = types.ReplyKeyboardRemove()
    global auto_model
    if m.text == '🔙Вернуться в начало':
        marks_buttons(bot, m)
    if m.text == '🚫Отсутствует в списке':
        sent = bot.send_message(m.chat.id, 'Пожалуйста, введите марку и модель авто с помощью клавиатуры...')
        bot.register_next_step_handler(sent, redkoe_auto)
    if m.text == 'Да, хочу!':
        zayavka_done(bot=bot, message=m) # функция оформления заявки. Отправляет админу специальное сообщение о заявке
        sent = bot.send_message(m.chat.id, '..', reply_markup=kb2)
        bot.register_next_step_handler(sent, sent_number)
    if m.text == 'AUDI':
        auto_model = 'AUDI'
        model_buttons(bot=bot, message=m, but1='A1, A2, A3, TT, A4, A5', but2='A6, A7, RS6, Q3, Q5, A8, R8',
                      but3='Q7, Q8, e-tron', but4='🚫Отсутствует в списке', but5='🔙Вернуться в начало').model_buttons()
    if m.text == 'BMW':
        auto_model = 'BMW'
        model_buttons(bot=bot, message=m, but1='2, 3, 4, Z, X1, X2', but2='5, 6, 7, X3, X4',
                      but3='X5, X6, X7', but4='🚫Отсутствует в списке', but5='🔙Вернуться в начало').model_buttons()
    if m.text == 'CHERY':
        auto_model = 'CHERY'
        model_buttons(bot=bot, message=m, but1='Amulet, Bonus, E5, Fora, Very', but2='Tiggo 1-4',
                      but3='Tiggo 7-8', but4='🚫Отсутствует в списке', but5='🔙Вернуться в начало').model_buttons()
    if m.text == 'CADILLAC':
        auto_model = 'CADILLAC'
        model_buttons(bot=bot, message=m, but1='CTS, ATS, BLS', but2='SRX, STS, XT4, XT5',
                      but3='Escalade, XT6', but4='🚫Отсутствует в списке', but5='🔙Вернуться в начало').model_buttons()
    if m.text == 'CHEVROLET':
        auto_model = 'CHEVROLET'
        model_buttons(bot=bot, message=m, but1='Aveo, Corvette, Camaro, Lacetti, Malibu',
                      but2='Spark, Niva, Cruze, Volt', but3='Evica, Orlando, Rezzo, Captiva',
                      but4='TrailBlazer, Tahoe, Traverse', but5='🚫Отсутствует в списке',
                      but6='🔙Вернуться в начало').model_buttons()
    if m.text == 'CHRYSLER':
        auto_model = 'CHRYSLER'
        model_buttons(bot=bot, message=m, but1='Neon, Sebring, Stratus, PT Cruiser',
                      but2='300C, Grand Voyager, Pacifica', but3='🚫Отсутствует в списке',
                      but4='🔙Вернуться в начало').model_buttons()
    if m.text == 'CITROEN':
        auto_model = 'CITROEN'
        model_buttons(bot=bot, message=m, but1='C1, C2, C3, C4, DS-4', but2='C6, Picasso, Berlingo, C5, DS-5',
                      but3='C-crosser', but4='🚫Отсутствует в списке', but5='🔙Вернуться в начало').model_buttons()
    if m.text == 'EXCEED':
        auto_model = 'EXCEED'
        model_buttons(bot=bot, message=m, but1='LX, TXL', but2='VX', but3='🚫Отсутствует в списке',
                      but4='🔙Вернуться в начало').model_buttons()
    if m.text == 'GEELY':
        auto_model = 'GEELY'
        model_buttons(bot=bot, message=m, but1='Coolray', but2='Tugella, Atlas', but3='🚫Отсутствует в списке',
                      but4='🔙Вернуться в начало').model_buttons()
    if m.text == 'FORD':
        auto_model = 'FORD'
        model_buttons(bot=bot, message=m, but1='Fusion, Focus, Fiesta, Mustang',
                      but2='Mondeo, Kuga, Maverick, Escape, S-Max', but3='Galaxy, Explorer',
                      but4='🚫Отсутствует в списке', but5='🔙Вернуться в начало').model_buttons()
    if m.text == 'HAVAL':
        auto_model = 'HAVAL'
        model_buttons(bot=bot, message=m, but1='Dargo', but2='F7, H6, H8, H9', but3='🚫Отсутствует в списке',
                      but4='🔙Вернуться в начало').model_buttons()
    if m.text == 'HONDA':
        auto_model = 'HONDA'
        model_buttons(bot=bot, message=m, but1='Accord, Jazz, Civic', but2='Crosstour, Legend, Element, HR-V, Prelude',
                      but3='CR-V', but4='🚫Отсутствует в списке', but5='🔙Вернуться в начало').model_buttons()
    if m.text == 'HYUNDAI':
        auto_model = 'HYUNDAI'
        model_buttons(bot=bot, message=m, but1='Accent, Getz, I30, I40, Atos, Solaris',
                      but2='Elantra, Sonata, Creta, Eques', but3='Genesis, Tucson, IX35, Matrix',
                      but4='Santa Fe, Palisade, IX55, Genesis GV70', but5='🚫Отсутствует в списке',
                      but6='🔙Вернуться в начало').model_buttons()
    if m.text == 'INFINITI':
        auto_model = 'INFINITI'
        model_buttons(bot=bot, message=m, but1='G, Q30', but2='FX, Q50, Q70, QX30, QX50, QX55', but3='JX70, QX70',
                      but4='🚫Отсутствует в списке', but5='🔙Вернуться в начало').model_buttons()

    if m.text == 'JAGUAR':
        auto_model = 'JAGUAR'
        model_buttons(bot=bot, message=m, but1='XF, F-type, F-pace', but2='XJ', but3='🚫Отсутствует в списке',
                      but4='🔙Вернуться в начало').model_buttons()
    if m.text == 'JEEP':
        auto_model = 'JEEP'
        model_buttons(bot=bot, message=m, but1='Wrangler, Liberty Compass, Cherokee', but2='🚫Отсутствует в списке',
                      but3='🔙Вернуться в начало').model_buttons()
    if m.text == 'KIA':
        auto_model = 'KIA'
        model_buttons(bot=bot, message=m, but1='Ceed, Cerato, Rio, Picanto',
                      but2='Optima, K5, K8, K900, Seltos, Sportage, Venga, Soul', but3='Carnival, Mohave, Sorento',
                      but4='🚫Отсутствует в списке', but5='🔙Вернуться в начало').model_buttons()
    if m.text == 'LADA':
        auto_model = 'LADA'
        model_buttons(bot=bot, message=m, but1='Granta, Kalina, Priora, Vesta, Largus, Niva, XRAY',
                      but2='🚫Отсутствует в списке', but3='🔙Вернуться в начало').model_buttons()
    if m.text == 'LAND ROVER':
        auto_model = 'LAND ROVER'
        model_buttons(bot=bot, message=m, but1='Freelander, Evoque', but2='Defender, Discovery, Range Rover, Velar',
                      but3='🚫Отсутствует в списке', but4='🔙Вернуться в начало').model_buttons()
    if m.text == 'LEXUS':
        auto_model = 'LEXUS'
        model_buttons(bot=bot, message=m, but1='IS, CT, LC', but2='RX, NX, ES, GS', but3='LS, LX, GX',
                      but4='🚫Отсутствует в списке', but5='🔙Вернуться в начало').model_buttons()
    if m.text == 'MAZDA':
        auto_model = 'MAZDA'
        model_buttons(bot=bot, message=m, but1='2, 3, MX-5', but2='5, 6, CX-3, CX-5', but3='CX-7, CX-9',
                      but4='🚫Отсутствует в списке', but5='🔙Вернуться в начало').model_buttons()
    if m.text == 'MERCEDES-BENZ':
        auto_model = 'MERCEDES-BENZ'
        model_buttons(bot=bot, message=m, but1='A, B, C, SLK, CLK, CLA', but2='E, GLK, GLA, SL, CLS, ML',
                      but3='GLE, GLC, R, S, CL', but4='🚫Отсутствует в списке',
                      but5='🔙Вернуться в начало').model_buttons()
    if m.text == 'MINI':
        auto_model = 'MINI'
        model_buttons(bot=bot, message=m, but1='Cooper',
                      but2='Countryman, Clubman', but3='🚫Отсутствует в списке',
                      but4='🔙Вернуться в начало').model_buttons()
    if m.text == 'MITSUBISHI':
        auto_model = 'MITSUBISHI'
        model_buttons(bot=bot, message=m, but1='Eclipse, Colt, Galant, Lancer',
                      but2='ASX, Eclipse Cross, Grandis, Space Star, Outlander',
                      but3='L-200, Outlander XL, Pajero, Pajero Sport', but4='🚫Отсутствует в списке',
                      but5='🔙Вернуться в начало').model_buttons()
    if m.text == 'NISSAN':
        auto_model = 'NISSAN'
        model_buttons(bot=bot, message=m, but1='Almera, Note, Tiida, Maxima, Micra', but2='Juke, Qashqai, 350Z, GT-R',
                      but3='Murano, Teana, X-Trail, Pathfinder, Patrol', but4='🚫Отсутствует в списке',
                      but5='🔙Вернуться в начало').model_buttons()
    if m.text == 'OPEL':
        auto_model = 'OPEL'
        model_buttons(bot=bot, message=m, but1='Astra, Corsa, Insignia', but2='Zafira, Omega, Vectra, Meriva',
                      but3='🚫Отсутствует в списке', but4='🔙Вернуться в начало').model_buttons()
    if m.text == 'PEUGEOT':
        auto_model = 'PEUGEOT'
        model_buttons(bot=bot, message=m, but1='107, 108, 206, 207, 3001, 308', but2='2008, 4008, 407, 508, Partner',
                      but3='🚫Отсутствует в списке', but4='🔙Вернуться в начало').model_buttons()
    if m.text == 'PORSCHE':
        auto_model = 'PORSCHE'
        model_buttons(bot=bot, message=m, but1='911, Cayman', but2='Macan, Panamera', but3='Cayenne',
                      but4='🚫Отсутствует в списке', but5='🔙Вернуться в начало').model_buttons()
    if m.text == 'RENAULT':
        auto_model = 'RENAULT'
        model_buttons(bot=bot, message=m, but1='Clio, Megane, Logan, Symbol, Sandero',
                      but2='Arkana, Captur, Duster, Kangoo, ', but3='Fluence, Scenic, Talisman, Laguna',
                      but4='Koleos', but5='🚫Отсутствует в списке', but6='🔙Вернуться в начало').model_buttons()
    if m.text == 'SKODA':
        auto_model = 'SKODA'
        model_buttons(bot=bot, message=m, but1='Fabia, Rapid, Ibiza', but2='Octavia, Karoq, Superb, Roomster, Yeti',
                      but3='Kodiaq', but4='🚫Отсутствует в списке', but5='🔙Вернуться в начало').model_buttons()
    if m.text == 'SEAT':
        auto_model = 'SEAT'
        model_buttons(bot=bot, message=m, but1='Altea, Freetrack, Ibiza, Leon', but2='🚫Отсутствует в списке',
                      but3='🔙Вернуться в начало').model_buttons()
    if m.text == 'SUBARU':
        auto_model = 'SUBARU'
        model_buttons(bot=bot, message=m, but1='Legacy', but2='Ascent, Forester, Outback, Impreza', but3='Tribeca',
                      but4='🚫Отсутствует в списке', but5='🔙Вернуться в начало').model_buttons()
    if m.text == 'TOYOTA':
        auto_model = 'TOYOTA'
        model_buttons(bot=bot, message=m, but1='Auris, Corolla, Yaris',
                      but2='Camry, Avensis, C-HR, Prius, Versa, GT86, Crown',
                      but3='Fortuner, LC100-300, Prado, Highlander', but4='🚫Отсутствует в списке',
                      but5='🔙Вернуться в начало').model_buttons()
    if m.text == 'VOLVO':
        auto_model = 'VOLVO'
        model_buttons(bot=bot, message=m, but1='C30, S40, V40', but2='C40, CC, S60, S80, S90, V50, V60, V70, XC40',
                      but3='XC60, XC70, XC90', but4='🚫Отсутствует в списке',
                      but5='🔙Вернуться в начало').model_buttons()
    if m.text == 'VOLKSWAGEN':
        auto_model = 'VOLKSWAGEN'
        model_buttons(bot=bot, message=m, but1='Polo, Scriocco, Beetle, Jetta, Golf',
                      but2='Passat, Arteon, Touran, Sharan, Golf plus, Tiguan', but3='Phaeton, Touareg',
                      but4='🚫Отсутствует в списке', but5='🔙Вернуться в начало').model_buttons()
    search_models(bot, m, m.text, auto_model=auto_model)  # класс опредляющий пригадлежность авто ценовым классам


@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback(callback):
    if callback.data == 'btn':
        bot.send_message(callback.message.chat.id, 'Спасибо! С Вами свяжутся в ближайшее время для уточнения информации')
        bot.send_message(admin_account, f'🚨!!!СРОЧНО!!!🚨\n'
                                       f'Хозяин, поступил запрос на участие в акции от:\n'
                                       f'Имя: {callback.from_user.first_name}\n'
                                       f'Фамилия: {callback.from_user.last_name}\n'
                                       f'Никнейм: {callback.from_user.username}\n'
                                       f'id чата: {callback.chat.id}\n'
                                       f'Ссылка: @{callback.from_user.username}\n'
                                       f'Быстрее уточни все необходимое и закрой заявку \n')


def redkoe_auto(message):  # функция регистрации заявки авто, которое отсутствует в каталоге бота
    global auto_model
    auto_model = message.text   # модели присваивается название введенное клиентов в сообщении
    bot.send_message(message.chat.id, 'Cпасибо! Я передал информацию мастеру. Прайс будет выслан Вам в ближайшее '
                                      'время.')
    bot.send_message(admin_account, f'🚨!!!СРОЧНО!!!🚨\n'
                                   f'Хозяин, поступил запрос прайса на отсутствующее в моем списке авто от:\n'
                                   f'Имя: {message.from_user.first_name}\n'
                                   f'Фамилия: {message.from_user.last_name}\n'
                                   f'Никнейм: {message.from_user.username}\n'
                                   f'id чата: {message.chat.id}\n'
                                   f'Ссылка: @{message.from_user.username}\n'
                                   f'Авто: {auto_model}\n'
                                   f'Быстрее отправь прайс на его корыто пока он не слился\n'
                                   f'В случае положительной отработки заявки не забудь перевести клиента из базы '
                                   f'"потенциальные клиенты" в базу "старые клиенты" с помощью команды\n '
                                   f'/next_level_base')
    clients_base(bot, message, auto_model).chec_and_record()  # класс проверки клиента в базе и его запись в базу
                                                              # в случае отсутствия


def base_perehvat(message):  # перехватчик текстовых сообщения с именем клиента для поиска его в базе
    clients_base(bot, message, auto_model, message.text).perevod_v_bazu()


def post_perehvat_1(message):  # перехватчик текста поста для рассылки
    global rasylka
    rasylka = rasylka_message(message.id)  # хз почему message.id а не message.text но bot.copy_message() работает только так
    model_buttons(bot, message).rasylka_buttons()  # вызов кнопок выбора базы для рассылки
    sent = bot.send_message(admin_account, 'Выберите базу для рассылки')
    bot.register_next_step_handler(sent, post_perehvat_2)


def post_perehvat_2(message):   # перехватчик сообщения с базой для рассылки
    clients_base(bot, rasylka.post, auto_model, message.text).rasylka_v_bazu()


def sent_message_perehvat_1(message):
    try:
        global rasylka
        rasylka = rasylka_message(message.text)
        sent = bot.send_message(admin_account, 'Введите текст сообщения')
        bot.register_next_step_handler(sent, sent_message_perehvat_2)
    except ValueError:
        bot.send_message(admin_account, 'Неккоректное значение. Воспользуйтесь командой /sent_message еще раз')


def sent_message_perehvat_2(message):
    kb2 = types.ReplyKeyboardRemove()
    global rasylka
    bot.copy_message(rasylka.post, admin_account, message.id, reply_markup=kb2)
    bot.send_message(admin_account, 'Птичка в клетке ✅')


def sent_number(message):
    bot.send_message(admin_account, 'Сообщение от клиента:')
    bot.copy_message(admin_account, message.chat.id, message.id)
    bot.send_message(message.chat.id, 'Сообщение доставлено ✅')



#if __name__ == '__main__':
    #scheduler = BackgroundScheduler()
    #scheduler.add_job(auto_voronka, "cron", day_of_week='mon-sun', hour=13)
    #scheduler.start()


#bot.polling()
bot.infinity_polling()

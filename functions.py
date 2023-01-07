from telebot import types
# библиотека работы с гугл таблицами
import gspread
# библиотека проверки даты
from datetime import *
# библиотека рандома
from random import *
from passwords import *

admin_account = igor


def marks_buttons(bot, message):  # функция определяющая клавиатуру с марками авто
    kb1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    but1 = types.KeyboardButton(text='AUDI')
    but2 = types.KeyboardButton(text='BMW')
    but3 = types.KeyboardButton(text='CADILLAC')
    but4 = types.KeyboardButton(text='CHERY')
    but5 = types.KeyboardButton(text='CHEVROLET')
    but6 = types.KeyboardButton(text='CHRYSLER')
    but7 = types.KeyboardButton(text='CITROEN')
    but8 = types.KeyboardButton(text='EXCEED')
    but9 = types.KeyboardButton(text='FORD')
    but10 = types.KeyboardButton(text='GEELY')
    but11 = types.KeyboardButton(text='HAVAL')
    but12 = types.KeyboardButton(text='HONDA')
    but13 = types.KeyboardButton(text='HYUNDAI')
    but14 = types.KeyboardButton(text='INFINITI')
    but15 = types.KeyboardButton(text='JAGUAR')
    but16 = types.KeyboardButton(text='JEEP')
    but17 = types.KeyboardButton(text='KIA')
    but18 = types.KeyboardButton(text='LADA')
    but19 = types.KeyboardButton(text='LAND ROVER')
    but20 = types.KeyboardButton(text='LEXUS')
    but21 = types.KeyboardButton(text='MAZDA')
    but22 = types.KeyboardButton(text='MERCEDES-BENZ')
    but23 = types.KeyboardButton(text='MINI')
    but24 = types.KeyboardButton(text='MITSUBISHI')
    but25 = types.KeyboardButton(text='NISSAN')
    but26 = types.KeyboardButton(text='OPEL')
    but27 = types.KeyboardButton(text='PEUGEOT')
    but28 = types.KeyboardButton(text='PORSCHE')
    but29 = types.KeyboardButton(text='RENAULT')
    but30 = types.KeyboardButton(text='SKODA')
    but31 = types.KeyboardButton(text='SUBARU')
    but32 = types.KeyboardButton(text='TOYOTA')
    but33 = types.KeyboardButton(text='VOLVO')
    but34 = types.KeyboardButton(text='VOLKSWAGEN')
    but35 = types.KeyboardButton(text='🚫Отсутствует в списке')
    kb1.add(but1, but2, but3, but4, but5, but6, but7, but8, but9, but10, but11, but12, but13, but14, but15, but16,
            but17, but18, but19, but20, but21, but22, but23, but24, but25, but26, but27, but28, but29, but30, but31,
            but32, but33, but34, but35)
    bot.send_message(message.chat.id, 'Пожалуйста выберите марку Вашего автомобиля', reply_markup=kb1)


class search_models: #класс определяющий принадлежность авто к классу
    klass_first = ['TT', 'X2', 'Bonus', 'ATS', 'Aveo', 'Spark', 'Neon', 'DS-4', 'Focus', 'Jazz', 'Atos', 'Q30', 'Rio', 'Granta',
                   'IS,', 'MX-5', 'SLK', 'Cooper', 'Colt', 'Tiida', 'Astra', '308', '911', 'Clio', 'Rapid', 'Legacy',
                   'Yaris', 'S40', 'Polo']
    klass_second = ['RS6', 'X4', 'Tiggo 1-4', 'XT5', 'Rezzo', 'Voyager', 'Picasso', 'TXL', 'Kuga', 'Coolray',
                    'Dargo', 'Prelude', 'Creta', 'Tucson', 'QX55', 'F-type', 'Venga', 'Evoque', 'GS', 'CX-3', 'GLA',
                    'Clubman', 'Grandis', 'Juke', 'Omega', 'Partner', 'Macan', 'Arkana', 'Laguna', 'Yeti', 'Impreza', 'Prius',
                    'V60', 'Tiguan']
    klass_third = ['e-tron', 'X6', 'Tiggo 7-8', 'Escalade', 'Tahoe', 'C-crosser', 'VX', 'Galaxy', 'Tugella',
                   'H9', 'CR-V', 'Palisade', 'JX70', 'XJ', 'Compass', 'Mohave', 'Velar', 'GX', 'CX-9', 'GLC', 'Pajero',
                   'Murano', 'Cayenne', 'Koleos', 'Kodiaq', 'Tribeca', 'Prado', 'XC90', 'Phaeton']
    klasses = [klass_first, klass_second, klass_third]

    def __init__(self, bot, message, text, auto_model):
        self.bot = bot
        self.message = message
        self.text = text
        self.list = list
        self.auto_model = auto_model
        for klass in self.klasses:
            for i in klass:
                if text.find(i) >= 0 and klass == self.klass_first:
                    file_open = open("1 class_.png", 'rb')
                    bot.send_photo(message.chat.id, file_open, f'Готово!\n'
                                                               f'Стоимость услуг для Вашего автомобиля {auto_model}\n'
                                                               'соответствует первому ценовому классу.\n'
                                                               f'/help - справка по боту \n'
                                                               f'/result - посмотреть на отзывы и результат работ')
                    model_buttons(self.bot, self.message).zayavka_buttons()  # вызов клавиш для оформления заявки
                    bot.send_message(admin_account, f'Хозяин! Замечена активность:\n'
                                                   f'Имя: {message.from_user.first_name}\n'
                                                   f'Фамилия: {message.from_user.last_name}\n'
                                                   f'Никнейм: {message.from_user.username}\n'
                                                   f'Ссылка: @{message.from_user.username}\n'
                                                   f'Авто: {auto_model} 1 класса')
                    # передача классу клиентской базы данных для поиска клиента в базе и записи в случае отсутствия
                    clients_base(self.bot, self.message, auto_model=self.auto_model + ' 1 класса').chec_and_record()

                if text.find(i) >= 0 and klass == self.klass_second:
                    file_open = open("2 class.png", 'rb')
                    bot.send_photo(message.chat.id, file_open, f'Готово!\n'
                                                               f'Стоимость услуг для Вашего автомобиля {auto_model}\n'
                                                               'соответствует второму ценовому классу.\n'
                                                               f'/help - справка по боту \n'
                                                               f'/result - посмотреть на отзывы и результат работ')
                    model_buttons(self.bot, self.message).zayavka_buttons()
                    bot.send_message(admin_account, f'Хозяин! Замечена активность:\n'
                                                    f'Имя: {message.from_user.first_name}\n'
                                                    f'Фамилия: {message.from_user.last_name}\n'
                                                    f'Никнейм: {message.from_user.username}\n'
                                                    f'Ссылка: @{message.from_user.username}\n'
                                                    f'Авто: {auto_model} 2 класса')
                    clients_base(self.bot, self.message, auto_model=self.auto_model + ' 2 класса').chec_and_record()

                if text.find(i) >= 0 and klass == self.klass_third:
                    file_open = open("3 class.png", 'rb')
                    bot.send_photo(message.chat.id, file_open, f'Готово!\n'
                                                               f'Стоимость услуг для Вашего автомобиля {auto_model}\n'
                                                               f'соответствует третьему ценовому классу.\n'
                                                               f'/help - справка по боту \n'
                                                               f'/result - посмотреть на отзывы и результат работ')
                    model_buttons(self.bot, self.message).zayavka_buttons()
                    bot.send_message(admin_account, f'Хозяин! Замечена активность:\n'
                                                    f'Имя: {message.from_user.first_name}\n'
                                                    f'Фамилия: {message.from_user.last_name}\n'
                                                    f'Никнейм: {message.from_user.username}\n'
                                                    f'Ссылка: @{message.from_user.username}\n'
                                                    f'Авто: {auto_model} 3 класса')
                    clients_base(self.bot, self.message, auto_model=self.auto_model + ' 3 класса').chec_and_record()


class model_buttons: # класс формирования клавиатур

    def __init__(self, bot, message, **kwargs):
        self.bot = bot
        self.message = message
        self.kwargs = kwargs

    def model_buttons(self):
        kb3 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        for key, value in self.kwargs.items():
            key = types.KeyboardButton(text=f'{value}')
            kb3.add(key)
        self.bot.send_message(self.message.chat.id, 'Пожалуйста выберите модель Вашего автомобиля', reply_markup=kb3)

    def zayavka_buttons(self):
        kb4 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        but1 = types.KeyboardButton(text='Да, хочу!')
        but2 = types.KeyboardButton(text='🔙Вернуться в начало')
        kb4.add(but1, but2)
        self.bot.send_message(self.message.chat.id, f'Хотите оставить заявку на интересующую(-ие) Вас услугу(-и)?\n',
                              reply_markup=kb4)

    def rasylka_buttons(self):
        kb5 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        but1 = types.KeyboardButton(text='Общая база клиентов')
        but2 = types.KeyboardButton(text='База потенциальных клиентов')
        but3 = types.KeyboardButton(text='База старых клиентов')
        kb5.add(but1, but2, but3)
        self.bot.send_message(self.message.chat.id, '...', reply_markup=kb5)


def zayavka_done(bot, message):
    if message.from_user.username is not None:
        bot.send_message(message.chat.id, f'Заявка оформлена и передана мастеру, с Вами свяжутся в ближайшее время. '
                                           'Спасибо, что выбрали нас.🤝\n'
                                          f'Для нового рассчета воспользуйтесь командой /price')
        bot.send_message(admin_account, f'🚨!!!СРОЧНО!!!🚨\n'
                                        f'Хозяин, поступила ЗАЯВКА от:\n'
                                        f'Псевдоним: @{message.from_user.username}\n'
                                        f'id чата: {message.chat.id}\n'
                                        f'Быстрее согласуй дату и закрой заявку пока он не слился'
                                        f'\n'
                                        f'В случае положительной отработки заявки не забудь перевести клиента из базы '
                                        f'"потенциальные клиенты" в базу "старые клиенты" с помощью команды\n '
                                        f'/next_level_base\n'
                                        f'/sent_message - отправить сообщение с помощью бота')
    else:
        bot.send_message(message.chat.id, f'Заявка оформлена и передана мастеру, пожалуйста перейдите в чат '
                                          f'@pogonin21 и напишите любое сообщение или отправьте в ответ на это '
                                          f'сообщение свой номер телефона в любом формате. '
                                          f'Спасибо, что выбрали нас.🤝\n'
                                          f'Для нового рассчета воспользуйтесь командой /price')
        bot.send_message(admin_account, f'🚨!!!СРОЧНО!!!🚨\n'
                                        f'Хозяин, поступила ЗАЯВКА от:\n'
                                        f'Псевдоним: @{message.from_user.username}\n'
                                        f'id чата: {message.chat.id}\n'
                                        f'Быстрее согласуй дату и закрой заявку пока он не слился\n'
                                        f'В случае положительной отработки заявки не забудь перевести клиента из базы '
                                        f'"потенциальные клиенты" в базу "старые клиенты" с помощью команды\n '
                                        f'/next_level_base\n'
                                        f'/sent_message - отправить сообщение с помощью бота')


class clients_base:  # класс базы данных

    def __init__(self, bot, message, auto_model, perehvat=None):
        self.bot = bot
        self.message = message
        self.auto_model = auto_model
        self.perehvat = perehvat
        gc = gspread.service_account(filename='base_key.json')  # доступ к гугл табл по ключевому файлу аккаунта разраба
        # открытие таблицы по юрл адресу:
        sh = gc.open('autoallure_dmd')
        self.worksheet = sh.worksheet('общая база клиентов')  # выбор листа 'общая база клиентов' таблицы
        self.worksheet2 = sh.worksheet('потенциальные клиенты')
        self.worksheet3 = sh.worksheet('старые клиенты')

    def chec_and_record(self):  # функция поиска и записи в базу
        worksheet_len = len(self.worksheet.col_values(1)) + 1  # поиск первой свободной ячейки для записи во 2 столбце
        worksheet_len2 = len(self.worksheet2.col_values(1)) + 1
        self.bot.send_message(admin_account, 'Пробиваю базу..')
        self.bot.send_message(admin_account, '...')
        if str(self.message.chat.id) in self.worksheet.col_values(1):
            self.bot.send_message(admin_account, ' Клиент есть в базе')
        else:
            self.bot.send_message(admin_account, f'Клиент добавлен в базу\n'
                    f'База: '
                    f'https://docs.google.com/spreadsheets/d/1M3PHqj06Ex1_oXKuyR8CZCjl4j67qxvQUNNfcA3WjyY/edit#gid=0')
            self.worksheet.update(f'A{worksheet_len}:F{worksheet_len}', [[self.message.chat.id, self.message.from_user.username,
                                             self.message.from_user.first_name, self.message.from_user.last_name,
                                             self.auto_model, str(datetime.now().date())]])
            self.worksheet2.update(f'A{worksheet_len2}:F{worksheet_len2}',
                                  [[self.message.chat.id, self.message.from_user.username,
                                    self.message.from_user.first_name, self.message.from_user.last_name,
                                    self.auto_model, str(datetime.now().date())]])

    def perevod_v_bazu(self):  # функция перевода из базы потенциальных клиентов в базу старых клиентов
        try:
            worksheet_len3 = len(self.worksheet3.col_values(1)) + 1
            cell = self.worksheet.find(self.perehvat)  # поиск ячейки с данными по ключевому слову
            # запись клиента в свободную строку базы старых клиентов:
            self.worksheet3.update(f'A{worksheet_len3}:F{worksheet_len3}', [self.worksheet.row_values(cell.row)])
            self.worksheet2.batch_clear([f"A{cell.row}:F{cell.row}"])  # удаление клиента из базы потенциальных
            self.bot.send_message(admin_account, 'Птичка в клетке ✅')
        except AttributeError:
            self.bot.send_message(admin_account, 'Ошибка, пользователь отсутствует, будь внимательнее если осознал свой '
                                                'косяк воспользуйся командой /next_level_base снова')

    def rasylka_v_bazu(self):  # функция рассылки постов в базы
        kb5 = types.ReplyKeyboardRemove()  # удаление клавиатуры
        kb6 = types.InlineKeyboardMarkup(row_width=1)
        but1 = types.InlineKeyboardButton(text='Конечно!', callback_data='btn')
        kb6.add(but1)
        if self.perehvat == 'Общая база клиентов':
            self.bot.send_message(admin_account, '...', reply_markup=kb5)
            for i in range(1, len(self.worksheet.col_values(1))):
                try:
                    self.bot.copy_message(self.worksheet.col_values(1)[i], admin_account, self.message, reply_markup=kb5)
                    #self.bot.send_message(self.worksheet.col_values(1)[i], 'Участвовать в акции?', reply_markup=kb6)
                except Exception as ex:
                    self.bot.send_message(admin_account, f'Босс, @{self.worksheet.col_values(2)[i]} заблочил меня \n'
                                                         f'Похоже настало время набить ебало...')
            self.bot.send_message(admin_account, 'Босс, рассылка в общую базу выполнена ✅')
        if self.perehvat == 'База потенциальных клиентов':
            self.bot.send_message(admin_account, '...', reply_markup=kb5)
            for i in range(1, len(self.worksheet.col_values(1))):
                try:
                    self.bot.copy_message(self.worksheet2.col_values(1)[i], admin_account, self.message, reply_markup=kb5)
                    #self.bot.send_message(self.worksheet2.col_values(1)[i], 'Участвовать в акции?', reply_markup=kb6)
                except Exception as ex:
                    self.bot.send_message(admin_account, f'Босс, @{self.worksheet2.col_values(2)[i]} заблочил меня \n'
                                                         f'Похоже настало время набить ебало...')
            self.bot.send_message(admin_account, 'Босс, рассылка в базу потенциальных клиентов выполнена ✅')
        if self.perehvat == 'База старых клиентов':
            self.bot.send_message(admin_account, '...', reply_markup=kb5)
            for i in range(0, len(self.worksheet.col_values(1))):
                try:
                    self.bot.copy_message(self.worksheet3.col_values(1)[i], admin_account, self.message, reply_markup=kb5)
                    #self.bot.send_message(self.worksheet3.col_values(1)[i], 'Участвовать в акции?', reply_markup=kb6)
                except Exception as ex:
                    self.bot.send_message(admin_account, f'Босс, @{self.worksheet3.col_values(2)[i]} заблочил меня \n'
                                                         f'Похоже настало время набить ебало...')
            self.bot.send_message(admin_account, 'Босс, рассылка в базу старых клиентов выполнена ✅')


class rasylka_message:  # класс хранения сообщения для рассылки
    def __init__(self, post):
        self.post = post

    def _get_message_(self):
        return self.post






#class auto_voronka:
    #def __init__(self, bot, day, month):
        #self.bot = bot
        #self.day = day
        #self.month = month
        #gc = gspread.service_account(filename='base_key.json')  # доступ к гугл табл по ключевому файлу аккаунта разраба
        # открытие таблицы по юрл адресу:
        #sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1M3PHqj06Ex1_oXKuyR8CZCjl4j67qxvQUNNfcA3WjyY/edit")
        #self.worksheet2 = sh.worksheet('потенциальные клиенты')
    #def voronka_potencialnye(self):
        #for i in range(1, len(self.worksheet2.col_values(1)))




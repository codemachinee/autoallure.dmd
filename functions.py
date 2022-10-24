from telebot import types


def marks_buttons(bot, message):
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


class search_models:
    klass_first = ['TT', 'X2', 'Bonus', 'ATS', 'Aveo', 'Spark', 'Neon', 'DS-4', 'Focus', 'Jazz', 'Atos', 'Q30', 'Rio', 'Granta',
                   'IS,', 'MX-5', 'SLK', 'Cooper', 'Colt', 'Tiida', 'Astra', '308', '911', 'Clio', 'Rapid', 'Legacy',
                   'Yaris', 'S40', 'Polo']
    klass_second = ['RS6', 'X4', 'Tiggo 1-4', 'XT5', 'Rezzo', 'Voyager', 'Picasso', 'TXL', 'Kuga', 'Coolray',
                    'Dargo', 'Prelude', 'Creta', 'Tucson', 'QX55', 'F-type', 'Venga', 'Evoque', 'GS', 'CX-3', 'GLA',
                    'Clubman', 'Grandis', 'Juke', 'Omega', 'Partner', 'Macan', 'Arkana', 'Laguna', 'Yeti', 'Impreza', 'Prius',
                    'V60', 'Tiguan']
    klass_third = ['e-tron', 'X6', 'Tiggo 7-8', 'Escalade', 'Tahoe', 'C-crosser', 'VX', 'Galaxy', 'Tugella',
                   'H9', 'CR-V', 'Palisade', 'JX70', 'XJ', 'Compass', 'Mohave', 'Velar', 'LX', 'CX-9', 'GLC', 'Pajero',
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
                                                               'соответствует первому ценовому классу.')
                    model_buttons(self.bot, self.message).zayavka_buttons()
                    bot.send_message('1338281106', f'Хозяин! Замечена активность:\n'
                                                   f'Имя: {message.from_user.first_name}\n'
                                                   f'Фамилия: {message.from_user.last_name}\n'
                                                   f'Псевдоним: @{message.from_user.username}\n'
                                                   f'Авто: {auto_model} 1 класса')

                if text.find(i) >= 0 and klass == self.klass_second:
                    file_open = open("2 class.png", 'rb')
                    bot.send_photo(message.chat.id, file_open, f'Готово!\n'
                                                               f'Стоимость услуг для Вашего автомобиля {auto_model}\n'
                                                               'соответствует второму ценовому классу.')
                    model_buttons(self.bot, self.message).zayavka_buttons()
                    bot.send_message('1338281106', f'Хозяин! Замечена активность:\n'
                                                   f'Имя: {message.from_user.first_name}\n'
                                                   f'Фамилия: {message.from_user.last_name}\n'
                                                   f'Псевдоним: @{message.from_user.username}\n'
                                                   f'Авто: {auto_model} 2 класса')

                if text.find(i) >= 0 and klass == self.klass_third:
                    file_open = open("3 class.png", 'rb')
                    bot.send_photo(message.chat.id, file_open, f'Готово!\n'
                                                               f'Стоимость услуг для Вашего автомобиля {auto_model}\n'
                                                               'соответствует третьему ценовому классу.')
                    model_buttons(self.bot, self.message).zayavka_buttons()
                    bot.send_message('1338281106', f'Хозяин! Замечена активность:\n'
                                                   f'Имя: {message.from_user.first_name}\n'
                                                   f'Фамилия: {message.from_user.last_name}\n'
                                                   f'Псевдоним: @{message.from_user.username}\n'
                                                   f'Авто: {auto_model} 3 класса')


class model_buttons:

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
        self.bot.send_message(self.message.chat.id, 'Хотите оставить заявку на интересующую(-ие) Вас услугу(-и)?',
                              reply_markup=kb4)


def zayavka_done(bot, message):
    kb2 = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, f'Заявка оформлена и передана мастеру, с Вами свяжутся в ближайшее время. '
                                      'Спасибо, что выбрали нас.🤝\n'
                                      f'Для нового рассчета воспользуйтесь командой /price', reply_markup=kb2)
    bot.send_message('1338281106', f'🚨!!!СРОЧНО!!!🚨\n'
                                   f'Хозяин, поступила ЗАЯВКА от:\n'
                                   f'Псевдоним: @{message.from_user.username}\n'
                                   f'Быстрее согласуй дату и закрой заявку пока он не слился')


#test





from datetime import datetime

import gspread
from aiogram import types

from handlers import admin_account


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

    async def chec_and_record(self):  # функция поиска и записи в базу
        worksheet_len = len(self.worksheet.col_values(1)) + 1  # поиск первой свободной ячейки для записи во 2 столбце
        worksheet_len2 = len(self.worksheet2.col_values(1)) + 1
        await self.bot.send_message(admin_account, 'Пробиваю базу..')
        await self.bot.send_message(admin_account, '...')
        if str(self.message.chat.id) in self.worksheet.col_values(1):
            await self.bot.send_message(admin_account, ' Клиент есть в базе')
        else:
            await self.bot.send_message(admin_account, f'Клиент добавлен в базу\n'
                                        f'База: https://docs.google.com/spreadsheets/d/1M3PHqj06Ex1_'
                                        f'oXKuyR8CZCjl4j67qxvQUNNfcA3WjyY/edit#gid=0')
            self.worksheet.update(f'A{worksheet_len}:F{worksheet_len}',
                                  [[self.message.chat.id, self.message.from_user.username,
                                    self.message.from_user.first_name, self.message.from_user.last_name,
                                    self.auto_model, str(datetime.now().date())]])
            self.worksheet2.update(f'A{worksheet_len2}:F{worksheet_len2}',
                                  [[self.message.chat.id, self.message.from_user.username,
                                  self.message.from_user.first_name, self.message.from_user.last_name,
                                 self.auto_model, str(datetime.now().date())]])

    async def perevod_v_bazu(self):  # функция перевода из базы потенциальных клиентов в базу старых клиентов
        try:
            worksheet_len3 = len(self.worksheet3.col_values(1)) + 1
            cell = self.worksheet.find(self.perehvat)  # поиск ячейки с данными по ключевому слову
            # запись клиента в свободную строку базы старых клиентов:
            self.worksheet3.update(f'A{worksheet_len3}:F{worksheet_len3}', [self.worksheet.row_values(cell.row)])
            self.worksheet2.batch_clear([f"A{cell.row}:F{cell.row}"])  # удаление клиента из базы потенциальных
            await self.bot.send_message(admin_account, 'Птичка в клетке ✅')
        except AttributeError:
            await self.bot.send_message(admin_account, 'Ошибка, пользователь отсутствует, будь внимательнее если осознал свой '
                                                'косяк воспользуйся командой /next_level_base снова')

    async def rasylka_v_bazu(self):  # функция рассылки постов в базы
        kb5 = types.ReplyKeyboardRemove()  # удаление клавиатуры
        kb6 = types.InlineKeyboardMarkup(row_width=1)
        but1 = types.InlineKeyboardButton(text='Конечно!', callback_data='btn')
        kb6.add(but1)
        if self.perehvat == 'Общая база клиентов':
            await self.bot.send_message(admin_account, '...', reply_markup=kb5)
            for i in range(1, len(self.worksheet.col_values(1))):
                try:
                    await self.bot.copy_message(self.worksheet.col_values(1)[i], admin_account, self.message, reply_markup=kb5)
                    #self.bot.send_message(self.worksheet.col_values(1)[i], 'Участвовать в акции?', reply_markup=kb6)
                except Exception as ex:
                    await self.bot.send_message(admin_account, f'Босс, @{self.worksheet.col_values(2)[i]} заблочил меня \n'
                                                         f'Похоже настало время набить ебало...')
            await self.bot.send_message(admin_account, 'Босс, рассылка в общую базу выполнена ✅')
        if self.perehvat == 'База потенциальных клиентов':
            await self.bot.send_message(admin_account, '...', reply_markup=kb5)
            for i in range(1, len(self.worksheet.col_values(1))):
                try:
                    await self.bot.copy_message(self.worksheet2.col_values(1)[i], admin_account, self.message, reply_markup=kb5)
                    #self.bot.send_message(self.worksheet2.col_values(1)[i], 'Участвовать в акции?', reply_markup=kb6)
                except Exception as ex:
                    await self.bot.send_message(admin_account, f'Босс, @{self.worksheet2.col_values(2)[i]} заблочил меня \n'
                                                         f'Похоже настало время набить ебало...')
            await self.bot.send_message(admin_account, 'Босс, рассылка в базу потенциальных клиентов выполнена ✅')
        if self.perehvat == 'База старых клиентов':
            await self.bot.send_message(admin_account, '...', reply_markup=kb5)
            for i in range(0, len(self.worksheet.col_values(1))):
                try:
                    await self.bot.copy_message(self.worksheet3.col_values(1)[i], admin_account, self.message, reply_markup=kb5)
                    #self.bot.send_message(self.worksheet3.col_values(1)[i], 'Участвовать в акции?', reply_markup=kb6)
                except Exception as ex:
                    await self.bot.send_message(admin_account, f'Босс, @{self.worksheet3.col_values(2)[i]} заблочил меня \n'
                                                         f'Похоже настало время набить ебало...')
            await self.bot.send_message(admin_account, 'Босс, рассылка в базу старых клиентов выполнена ✅')
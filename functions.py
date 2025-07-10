import asyncio
from datetime import datetime

import gspread
from gspread.exceptions import APIError
from loguru import logger

from passwords import igor, kostya, loggs_acc

# admin_account = igor


class clients_base:  # класс базы данных

    def __init__(self, bot, message, auto_model=None):
        self.bot = bot
        self.message = message
        self.auto_model = auto_model
        self.worksheet = None
        self.worksheet2 = None
        self.worksheet3 = None

    async def connect_to_google(self):
        for attempt in range(5):
            try:
                gc = gspread.service_account(filename='base_key.json')  # доступ к гугл табл по ключевому файлу аккаунта разраба
                # открытие таблицы по юрл адресу:
                sh = gc.open('autoallure_dmd')
                self.worksheet = sh.worksheet('общая база клиентов')  # выбор листа 'общая база клиентов' таблицы
                self.worksheet2 = sh.worksheet('потенциальные клиенты')
                self.worksheet3 = sh.worksheet('старые клиенты')
                return
            except APIError as e:
                if e.response.status_code == 503:  # Если сервис временно недоступен
                    print(f"Google API недоступен, попытка {attempt + 1}/{5}...")
                    await asyncio.sleep(2)  # Ждем перед новой попыткой
                else:
                    raise  # Если другая ошибка, выбрасываем
        raise RuntimeError("Не удалось подключиться к Google Sheets после нескольких попыток.")

    async def chec_and_record(self):  # функция поиска и записи в базу
        await self.connect_to_google()
        try:
            worksheet_len = len(self.worksheet.col_values(1)) + 1  # поиск первой свободной ячейки для записи во 2 столбце
            worksheet_len2 = len(self.worksheet2.col_values(1)) + 1
            await self.bot.send_message(admin_account.admin, 'Пробиваю базу..')
            await self.bot.send_message(admin_account.admin, '...')
            if str(self.message.chat.id) in self.worksheet.col_values(1):
                await self.bot.send_message(admin_account.admin, ' Клиент есть в базе')
            else:
                await self.bot.send_message(admin_account.admin, 'Клиент добавлен в базу\n'
                                            'База: https://docs.google.com/spreadsheets/d/1M3PHqj06Ex1_'
                                            'oXKuyR8CZCjl4j67qxvQUNNfcA3WjyY/edit#gid=0')
                self.worksheet.update(f'A{worksheet_len}:F{worksheet_len}',
                                      [[self.message.chat.id, self.message.chat.username,
                                        self.message.chat.first_name, self.message.chat.last_name,
                                        self.auto_model, str(datetime.now().date())]])
                self.worksheet2.update(f'A{worksheet_len2}:F{worksheet_len2}',
                                      [[self.message.chat.id, self.message.chat.username,
                                      self.message.chat.first_name, self.message.chat.last_name,
                                     self.auto_model, str(datetime.now().date())]])
        except Exception as e:
            logger.exception('Ошибка в functions/chec_and_record', e)
            await self.bot.send_message(loggs_acc, f'Ошибка в functions/chec_and_record: {e}')

    async def perevod_v_bazu(self, nickname):  # функция перевода из базы потенциальных клиентов в базу старых клиентов
        mess = await self.bot.send_message(admin_account.admin, 'загрузка..🚀')
        await self.connect_to_google()
        try:
            worksheet_len3 = len(self.worksheet3.col_values(1)) + 1
            cell = self.worksheet2.find(nickname)  # поиск ячейки с данными по ключевому слову
            # запись клиента в свободную строку базы старых клиентов:
            self.worksheet3.update(f'A{worksheet_len3}:F{worksheet_len3}', [self.worksheet2.row_values(cell.row)])
            self.worksheet2.batch_clear([f"A{cell.row}:F{cell.row}"])  # удаление клиента из базы потенциальных
            await self.bot.edit_message_text(text='Птичка в клетке ✅', chat_id=admin_account.admin, message_id=mess.message_id)
        except AttributeError:
            await self.bot.edit_message_text(chat_id=admin_account.admin, text='Ошибка, пользователь отсутствует, будь внимательнее если осознал свой '
                                                'косяк воспользуйся командой /next_level_base снова', message_id=mess.message_id)
        except Exception as e:
            logger.exception('Ошибка в functions/perevod_v_bazu', e)
            await self.bot.send_message(loggs_acc, f'Ошибка в functions/perevod_v_bazu: {e}')

    async def rasylka_v_bazu(self, base):  # функция рассылки постов в базы
        mess = await self.bot.send_message(admin_account.admin, 'загрузка..🚀')
        await self.connect_to_google()
        try:
            if base == 'Общая база клиентов':
                for i in range(1, len(self.worksheet.col_values(1))):
                    try:
                        await asyncio.sleep(0.3)
                        await self.bot.copy_message(self.worksheet.col_values(1)[i], admin_account.admin, self.message.message_id)
                    except Exception:
                        await self.bot.bot.send_message(chat_id=admin_account.admin, text=f'Босс, '
                                                         f'@{self.worksheet.col_values(2)[i]} заблочил меня \n'
                                                         f'Похоже настало время набить ебало...')
                await self.bot.edit_message_text(chat_id=admin_account.admin, text='Босс, рассылка в общую базу выполнена ✅',
                                                 message_id=mess.message_id)
            elif base == 'База потенциальных клиентов':
                for i in range(1, len(self.worksheet2.col_values(1))):
                    try:
                        await asyncio.sleep(0.3)
                        await self.bot.copy_message(self.worksheet2.col_values(1)[i], admin_account.admin, self.message.message_id)
                        #self.bot.send_message(self.worksheet2.col_values(1)[i], 'Участвовать в акции?', reply_markup=kb6)
                    except Exception:
                        await self.bot.edit_message_text(chat_id=admin_account.admin, text=f'Босс, '
                                                         f'@{self.worksheet.col_values(2)[i]} заблочил меня \n'
                                                         f'Похоже настало время набить ебало...', message_id=mess.message_id)
                await self.bot.edit_message_text(chat_id=admin_account.admin, text='Босс, рассылка в общую базу выполнена ✅',
                                                 message_id=mess.message_id)
            elif base == 'База старых клиентов':
                for i in range(1, len(self.worksheet3.col_values(1))):
                    try:
                        await asyncio.sleep(0.3)
                        await self.bot.copy_message(self.worksheet3.col_values(1)[i], admin_account.admin, self.message.message_id)
                        #self.bot.send_message(self.worksheet3.col_values(1)[i], 'Участвовать в акции?', reply_markup=kb6)
                    except Exception:
                        await self.bot.edit_message_text(chat_id=admin_account.admin, text=f'Босс, '
                                                         f'@{self.worksheet.col_values(2)[i]} заблочил меня \n'
                                                         f'Похоже настало время набить ебало...', message_id=mess.message_id)
                await self.bot.edit_message_text(chat_id=admin_account.admin, text='Босс, рассылка в общую базу выполнена ✅',
                                                 message_id=mess.message_id)
        except Exception as e:
            logger.exception('Ошибка в functions/rasylka_v_bazu', e)
            await self.bot.send_message(loggs_acc, f'Ошибка в functions/rasylka_v_bazu: {e}')


class Admin_acc:
    def __init__(self):
        self.admin = kostya

    async def get_admin(self):
        return self.admin

    async def set_admin(self):
        if self.admin == kostya:
            self.admin = igor
        else:
            self.admin = kostya


admin_account = Admin_acc()


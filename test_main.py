from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from FSM import step_message
from loguru import logger

from passwords import*
# Удаляем стандартный обработчик
logger.remove()
# Настраиваем логирование в файл с ограничением количества файлов
logger.add(
    "loggs.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
    rotation="5 MB",  # Ротация файла каждые 10 MB
    retention="10 days",  # Хранить только 5 последних логов
    compression="zip",  # Сжимать старые логи в архив
    backtrace=True,     # Сохранение трассировки ошибок
    diagnose=True       # Подробный вывод
)


# token = lemonade
token = codemashine_test

bot = Bot(token=token)
dp = Dispatcher()

db = Database()


@dp.message(Command(commands='start'))
async def start(message):
    if message.chat.id in admins_list:
        # await send_news()
        await bot.send_message(message.chat.id, f'<b>Бот-поддержки продаж инициализирован.</b>\n'
                               f'<b>Режим доступа</b>: Администратор\n'
                               f'/help - справка по боту', message_thread_id=message.message_thread_id,
                               parse_mode='html')
    else:
        data_from_database = await Database().search_in_table(message.chat.id)
        if data_from_database is not False and data_from_database[0][4] >= 6:
            pass
        else:
            await bot.send_message(message.chat.id, f'<b>Здравствуйте {message.from_user.first_name}!</b>\n\n'
                                   f'<b>Бот-поддержки клиентов</b> инициализирован.\n'
                                   f'/help - справка по боту', message_thread_id=message.message_thread_id,
                                   parse_mode='html')
            await bot.send_message(message.chat.id, f'Пожалуйста выберите интересующий товар:',
                                   message_thread_id=message.message_thread_id, reply_markup=kb_choice_tovar)
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from passwords import*
# from functions import*
from handlers import *
from loggs import *


# token = autoallure
token = codemashine_test

bot = Bot(token=token)
dp = Dispatcher()


dp.message.register(start, Command(commands='start'))
dp.message.register(help, Command(commands='help'))
dp.message.register(price, Command(commands='price'))
dp.message.register(result, Command(commands='result'))
dp.callback_query.register(check_callback, Form_registration.registration_geo)
dp.callback_query.register(check_callbacks, F.data)
dp.message.register(check_message, F.text)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        logger.info('включение бота')
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.exception('выключение бота')
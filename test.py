import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from passwords import *

TOKEN = codemashine_test

bot = Bot(token=TOKEN)
dp = Dispatcher()


# Главная команда /start
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Открыть Web App", web_app=WebAppInfo(url="https://taplink.cc/lubov.i.golubi"))]
    ])

    await message.answer("Нажми на кнопку ниже, чтобы открыть Web App:", reply_markup=keyboard)


# Обработка данных, полученных из Web App
@dp.message()
async def web_app_data_handler(message: types.Message):
    if message.web_app_data:
        data = message.web_app_data.data  # Получаем JSON данные
        await message.answer(f"✅ Получены данные из Web App: {data}")


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
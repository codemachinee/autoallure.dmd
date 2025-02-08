from aiogram import Bot, Dispatcher, F
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.filters import Command
from handlers import *

from FSM import *
from database import *


# token = autoallure
token = codemashine_test

bot = Bot(token=token)
dp = Dispatcher()


dp.message.register(start, Command(commands='start'))
dp.message.register(help, Command(commands='help'))
dp.message.register(price, Command(commands='price'))
dp.message.register(result, Command(commands='result'))
dp.message.register(post, Command(commands='post'))
dp.message.register(sent_message, Command(commands='sent_message'))
dp.message.register(next_level_base, Command(commands='next_level_base'))
dp.message.register(day_visitors, Command(commands='day_visitors'))
dp.message.register(reset_cash, Command(commands='reset_cash'))

dp.message.register(anoter_model_registration, Another_model.model)

dp.message.register(message_from_user, Another_model.message)

dp.message.register(rassylka, Rassylka.post)

dp.message.register(message_from_admin_chat, Message_from_admin.user_id)
dp.message.register(message_from_admin_text, Message_from_admin.message)

dp.callback_query.register(check_callbacks, Another_model.marka)
dp.callback_query.register(check_callbacks, Another_model.model)
dp.callback_query.register(check_callbacks, Rassylka.post)

dp.callback_query.register(check_callbacks, F.data)

dp.message.register(next_level, Next_level_base.nickname)

dp.message.register(check_message, F.text)


async def main():
    await db.chek_tables()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(db.delete_all_users, "cron", day_of_week='mon-sun', hour=00)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        logger.info('включение бота')
        asyncio.run(main())
    except KeyboardInterrupt:
        asyncio.run(db.close())
        logger.exception('выключение бота')
        bot.send_message(loggs_acc, f'выключение бота')

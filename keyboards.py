import asyncio
import json

import aiofiles
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from passwords import *
admin_account = igor
# admin_account = kostya

kb_price = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=' AUDI', callback_data='AUDI'),
                InlineKeyboardButton(text='️BMW', callback_data='BMW'),
                InlineKeyboardButton(text='CADILLAC', callback_data='CADILLAC')],
                [InlineKeyboardButton(text='CHANGAN', callback_data='CHANGAN'),
                InlineKeyboardButton(text='CHERY', callback_data="CHERY"),
                InlineKeyboardButton(text='️CHEVROLET', callback_data='CHEVROLET')],
                [InlineKeyboardButton(text='CHRYSLER', callback_data='CHRYSLER'),
                InlineKeyboardButton(text='CITROEN', callback_data='CITROEN'),
                InlineKeyboardButton(text='️EXEED', callback_data='EXEED')],
                [InlineKeyboardButton(text='FORD', callback_data='FORD'),
                InlineKeyboardButton(text='GAC', callback_data='GAC'),
                InlineKeyboardButton(text='GEELY', callback_data='GEELY')],
                [InlineKeyboardButton(text='️HAVAL', callback_data="HAVAl"),
                InlineKeyboardButton(text='HONDA', callback_data='HONDA'),
                InlineKeyboardButton(text='HUMMER', callback_data='HUMMER')],
                [InlineKeyboardButton(text='️HYUNDAI', callback_data='HYUNDAI'),
                InlineKeyboardButton(text='INFINITI', callback_data='INFINITI'),
                InlineKeyboardButton(text='JAECOO', callback_data='JAECOO')],
                [InlineKeyboardButton(text='JAGUAR', callback_data='JAGUAR'),
                InlineKeyboardButton(text='️JEEP', callback_data='JEEP'),
                InlineKeyboardButton(text='KIA', callback_data='KIA')],
                [InlineKeyboardButton(text='️➡️', callback_data='page_two')]
            ])

kb_price_two = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='LADA', callback_data='LADA'),
     InlineKeyboardButton(text='️LAND ROVER', callback_data='LAND ROVER'),
     InlineKeyboardButton(text='LEXUS', callback_data='LEXUS')],
    [InlineKeyboardButton(text='LIXIANG', callback_data='LIXIANG'),
     InlineKeyboardButton(text='MAZDA', callback_data='MAZDA'),
     InlineKeyboardButton(text='MINI', callback_data='MINI')],
    [InlineKeyboardButton(text='MITSUBISHI', callback_data='MITSUBISHI'),
     InlineKeyboardButton(text='️NISSAN', callback_data='NISSAN'),
     InlineKeyboardButton(text='OMODA', callback_data='OMODA')],
    [InlineKeyboardButton(text='OPEL', callback_data='OPEL'),
     InlineKeyboardButton(text='PEUGEOT', callback_data='PEUGEOT'),
     InlineKeyboardButton(text='PORSCHE', callback_data='PORSCHE')],
    [InlineKeyboardButton(text='RENAULT', callback_data='RENAULT'),
     InlineKeyboardButton(text='SKODA', callback_data='SKODA'),
     InlineKeyboardButton(text='️SUBARU', callback_data='SUBARU')],
    [InlineKeyboardButton(text='TANK', callback_data='TANK'),
     InlineKeyboardButton(text='TOYOTA', callback_data='TOYOTA'),
     InlineKeyboardButton(text='VOLVO', callback_data='VOLVO')],
    [InlineKeyboardButton(text='️MERCEDES-BENZ', callback_data='MERCEDES-BENZ'),
     InlineKeyboardButton(text='VOLKSWAGEN', callback_data='VOLKSWAGEN')],
    [InlineKeyboardButton(text='️⬅️️', callback_data='page_one')]
])


class Buttons:
    def __init__(self, bot, message):
        self.bot = bot
        self.message = message

    async def marka_buttons(self, next_button=None, back_button=None):
        if back_button is None and next_button is not None:
            kb_marks = kb_price
        elif back_button is not None and next_button is None:
            kb_marks = kb_price_two
        await self.bot.edit_message_reply_markup(chat_id=self.message.chat.id, message_id=self.message.message_id,
                                                 reply_markup=kb_marks)

    async def models_buttons(self, marka):
        keyboard_list = []
        async with aiofiles.open('price.json', "r", encoding="utf-8") as file:
            content = await file.read()
            data = json.loads(content)
            keys_list = list(data.keys())
            data = data[marka]
            for i in data:
                if i is None:
                    pass
                else:
                    keyboard_list.append([types.InlineKeyboardButton(text=', '.join(i),
                                                                     callback_data=f"{data.index(i) + 1}_class")])
            another_button = types.InlineKeyboardButton(text="🚫Отсутствует в списке", callback_data=f'another_{marka}')
            if keys_list.index(marka) < 21:
                back_value_button = types.InlineKeyboardButton(text="↩️ Вернуться", callback_data='price_menu')
            else:
                back_value_button = types.InlineKeyboardButton(text="↩️ Вернуться", callback_data='price_menu_two')
            keyboard_list.append([another_button])
            keyboard_list.append([back_value_button])
            kb_models_buttons = types.InlineKeyboardMarkup(inline_keyboard=keyboard_list)
            await self.bot.edit_message_text(chat_id=self.message.chat.id, text=f'Пожалуйста выберите модель Вашего '
                                                                                f'автомобиля 🚙:',
                                             message_id=self.message.message_id, reply_markup=kb_models_buttons)

    async def zayavka_buttons(self, marka):
        kb_zayavka = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='✅ Да, оставить завку!', callback_data='zayavka_yes'),
             InlineKeyboardButton(text='️↩️ Вернуться', callback_data=marka)]])
        await self.bot.send_message(self.message.chat.id, f'Хотите оставить заявку на интересующую(-ие) Вас услугу(-и)?\n',
                                    reply_markup=kb_zayavka)
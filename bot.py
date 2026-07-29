from aiogram import Bot, Dispatcher, types

from aiogram.filters import Command

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import asyncio
import os
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)

dp = Dispatcher()

@dp.message(Command("start"))

async def start(message: types.Message):

    keyboard = InlineKeyboardMarkup(

        inline_keyboard=[

            [

                InlineKeyboardButton(

                    text="🇺🇦 Українська",

                    callback_data="uk"

                )

            ],

            [

                InlineKeyboardButton(

                    text="🇬🇧 English",

                    callback_data="en"

                )

            ],

            [

                InlineKeyboardButton(

                    text="🇱🇹 Lietuvių",

                    callback_data="lt"

                )

            ]

        ]

    )

    await message.answer(

        "👋 Вітаємо у ресторані Kyiv! 🇺🇦\n\n"

        "Оберіть мову:",

        reply_markup=keyboard

    )

@dp.callback_query()

async def language(callback: types.CallbackQuery):

    if callback.data == "uk":

        await callback.message.answer(

            "Чи сподобався вам візит?\n\n"

            "Оберіть оцінку ⭐️"

        )

    await callback.answer()

async def main():

    await dp.start_polling(bot)

if name == "__main__":

    asyncio.run(main())

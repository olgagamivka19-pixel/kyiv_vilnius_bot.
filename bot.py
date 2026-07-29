from aiogram import Bot, Dispatcher, types

from aiogram.filters import Command

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import asyncio
import os
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = -5179615999
bot = Bot(token=TOKEN)

dp = Dispatcher()
CHAT_ID = 5179615999
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

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="⭐️ 1", callback_data="rating_1"),
                    InlineKeyboardButton(text="⭐️ 2", callback_data="rating_2"),
                    InlineKeyboardButton(text="⭐️ 3", callback_data="rating_3")
                ],
                [
                    InlineKeyboardButton(text="⭐️ 4", callback_data="rating_4"),
                    InlineKeyboardButton(text="⭐️ 5", callback_data="rating_5")
                ]
            ]
        )

        await callback.message.answer(
            "Чи сподобався вам візит?\n\n"
            "Оберіть оцінку ⭐️",
            reply_markup=keyboard
        )


    elif callback.data.startswith("rating_"):

        rating = callback.data.split("_")[1]

        if rating in ["1", "2", "3"]:

            await bot.send_message(
               ADMIN_CHAT_ID,
                f"⚠️ Новий відгук Kyiv\n\n"
                f"Оцінка клієнта: ⭐️{rating}"
            )

            await callback.message.answer(
                "Дякуємо за ваш відгук.\n"
                "Нам шкода, що ваш візит не виправдав очікувань.\n\n"
                "Напишіть, будь ласка, що ми можемо покращити."
            )

        else:

            await callback.message.answer(
                "Дякуємо за високу оцінку 🤍\n\n"
                "Будемо вдячні за ваш відгук у Google ⭐️"
            )


    await callback.answer()


# Тимчасово для отримання ID групи
@dp.message()
async def get_chat_id(message: types.Message):
    await message.answer(f"ID чату: {message.chat.id}")


async def main():
    await dp.start_polling(bot)


if __name__== "__main__":
    asyncio.run(main())

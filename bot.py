from aiogram import Bot, Dispatcher, types

from aiogram.filters import Command

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import asyncio

import os

TOKEN = os.getenv("BOT_TOKEN")

ADMIN_CHAT_ID = -5179615999

bot = Bot(token=TOKEN)

dp = Dispatcher()

user_language = {}

waiting_feedback = set()

def lang_buttons():

    return InlineKeyboardMarkup(

        inline_keyboard=[

            [InlineKeyboardButton(text="🇺🇦 Українська", callback_data="uk")],

            [InlineKeyboardButton(text="🇬🇧 English", callback_data="en")],

            [InlineKeyboardButton(text="🇱🇹 Lietuvių", callback_data="lt")]

        ]

    )

def rating_buttons():

    return InlineKeyboardMarkup(

        inline_keyboard=[

            [

                InlineKeyboardButton(text="⭐️1", callback_data="rating_1"),

                InlineKeyboardButton(text="⭐️2", callback_data="rating_2"),

                InlineKeyboardButton(text="⭐️3", callback_data="rating_3")

            ],

            [

                InlineKeyboardButton(text="⭐️4", callback_data="rating_4"),

                InlineKeyboardButton(text="⭐️5", callback_data="rating_5")

            ]

        ]

    )

@dp.message(Command("start"))

async def start(message: types.Message):

    await message.answer(

        "👋 Вітаємо у ресторані Kyiv!\n\nОберіть мову:",

        reply_markup=lang_buttons()

    )

@dp.callback_query()

async def callback_handler(callback: types.CallbackQuery):

    user_id = callback.from_user.id

    if callback.data in ["uk", "en", "lt"]:

        user_language[user_id] = callback.data

        text = {

            "uk": "Чи сподобався вам ваш візит?\n\nОберіть оцінку ⭐️",

            "en": "Did you enjoy your visit?\n\nChoose your rating ⭐️",

            "lt": "Ar jums patiko jūsų apsilankymas?\n\nPasirinkite įvertinimą ⭐️"

        }

        await callback.message.answer(

            text[callback.data],

            reply_markup=rating_buttons()

        )

    elif callback.data.startswith("rating_"):

        rating = callback.data.split("_")[1]

        lang = user_language.get(user_id, "uk")

        if rating in ["1", "2", "3"]:

            waiting_feedback.add(user_id)

            text = {

                "uk": "Нам шкода, що ваш візит не виправдав очікувань 😔\n\nОпишіть, будь ласка, ситуацію. Можете також додати фото 📸",

                "en": "We are sorry your visit did not meet expectations 😔\n\nPlease describe the situation. You can also add a photo 📸",

                "lt": "Apgailestaujame, kad jūsų apsilankymas neatitiko lūkesčių 😔\n\nPrašome aprašyti situaciją. Galite pridėti nuotrauką 📸"

            }

            await callback.message.answer(text[lang])
            else:

            text = {

                "uk": "Дякуємо за високу оцінку 🤍\n\nБудемо вдячні за відгук у Google ⭐️",

                "en": "Thank you for your high rating 🤍\n\nWe would appreciate your Google review ⭐️",

                "lt": "Dėkojame už aukštą įvertinimą 🤍\n\nBūtume dėkingi už atsiliepimą Google ⭐️"

            }

            button = {

                "uk": "⭐️ Залишити відгук Google",

                "en": "⭐️ Leave Google review",

                "lt": "⭐️ Palikti atsiliepimą Google"

            }

            google = InlineKeyboardMarkup(

                inline_keyboard=[

                    [

                        InlineKeyboardButton(

                            text=button[lang],

                            url="https://search.google.com/local/writereview?placeid=ChIJh2pRZtOV3UYR9-p0eIiDA2o"

                        )

                    ]

                ]

            )

            await callback.message.answer(

                text[lang],

                reply_markup=google

            )

    await callback.answer()

@dp.message()

async def receive_feedback(message: types.Message):

    user_id = message.from_user.id

    if user_id in waiting_feedback:

        waiting_feedback.remove(user_id)

        info = (

            "⚠️ Новий негативний відгук Kyiv\n\n"

            f"Клієнт: {message.from_user.full_name}\n"

        )

        if message.photo:

            await bot.send_photo(

                ADMIN_CHAT_ID,

                message.photo[-1].file_id,

                caption=info + "\n" + (message.caption or "")

            )

        elif message.text:

            await bot.send_message(

                ADMIN_CHAT_ID,

                info + "\n" + message.text

            )

        await message.answer(

            "Дякуємо за ваш відгук 🙂\n"

            "Інформацію передано керівництву ресторану."

        )

async def main():

    await dp.start_polling(bot)

if __name__ == "__main__":

    asyncio.run(main())

from aiogram import Bot, Dispatcher, types

from aiogram.filters import Command

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import asyncio

import os

TOKEN = os.getenv("BOT_TOKEN")

ADMIN_CHAT_ID = -5179615999

bot = Bot(token=TOKEN)

dp = Dispatcher()

# зберігаємо мову і очікування відгуку

user_language = {}

waiting_feedback = {}

def ratings_keyboard():

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

        "👋 Вітаємо у ресторані Kyiv!\n\n"

        "Оберіть мову:",

        reply_markup=keyboard

    )

@dp.callback_query()

async def callback_handler(callback: types.CallbackQuery):

    user_id = callback.from_user.id

    # Вибір мови

    if callback.data in ["uk", "en", "lt"]:

        user_language[user_id] = callback.data

        if callback.data == "uk":

            text = (

                "Чи сподобався вам ваш візит?\n\n"

                "Оберіть оцінку ⭐️"

            )

        elif callback.data == "en":

            text = (

                "Did you enjoy your visit?\n\n"

                "Choose your rating ⭐️"

            )

        else:

            text = (

                "Ar jums patiko jūsų apsilankymas?\n\n"

                "Pasirinkite įvertinimą ⭐️"

            )

        await callback.message.answer(

            text,

            reply_markup=ratings_keyboard()

        )

    # Оцінка

    elif callback.data.startswith("rating_"):

        rating = callback.data.split("_")[1]

        lang = user_language.get(user_id, "uk")

        if rating in ["1", "2", "3"]:

            waiting_feedback[user_id] = True

            if lang == "uk":

                text = (

                    "Нам шкода, що ваш візит не виправдав очікувань 😔\n\n"

                    "Будь ласка, опишіть ситуацію.\n"

                    "Ви також можете додати фото 📸"

                )

            elif lang == "en":

                text = (

                    "We are sorry that your visit did not meet expectations 😔\n\n"

                    "Please describe the situation.\n"

                    "You can also attach a photo 📸"

                )

            else:

                text = (

                    "Apgailestaujame, kad jūsų apsilankymas neatitiko lūkesčių 😔\n\n"

                    "Prašome aprašyti situaciją.\n"

                    "Taip pat galite pridėti nuotrauką 📸"

                )

            await callback.message.answer(text)

        else:

            if lang == "uk":

                text = (

                    "Дякуємо за високу оцінку 🤍\n\n"

                    "Будемо вдячні за ваш відгук у Google ⭐️"

                )

                button = "⭐️ Залишити відгук Google"

            elif lang == "en":

                text = (

                    "Thank you for your high rating 🤍\n\n"

                    "We would appreciate your Google review ⭐️"

                )
                button = "⭐️ Leave Google review"

            else:

                text = (

                    "Dėkojame už aukštą įvertinimą 🤍\n\n"

                    "Būtume dėkingi už jūsų atsiliepimą Google ⭐️"

                )

                button = "⭐️ Palikti atsiliepimą Google"

            google_button = InlineKeyboardMarkup(

                inline_keyboard=[

                    [

                        InlineKeyboardButton(

                            text=button,

                            url="https://search.google.com/local/writereview?placeid=ChIJh2pRZtOV3UYR9-p0eIiDA2o"

                        )

                    ]

                ]

            )

            await callback.message.answer(

                text,

                reply_markup=google_button

            )

    await callback.answer()

# Отримання тексту або фото від клієнта

@dp.message()

async def receive_feedback(message: types.Message):

    user_id = message.from_user.id

    if waiting_feedback.get(user_id):

        waiting_feedback[user_id] = False

        caption = (

            "⚠️ Новий негативний відгук Kyiv\n\n"

            f"Клієнт: {message.from_user.full_name}\n"

            f"ID: {user_id}\n\n"

        )

        if message.text:

            await bot.send_message(

                ADMIN_CHAT_ID,

                caption + message.text

            )

        elif message.photo:

            await bot.send_photo(

                ADMIN_CHAT_ID,

                photo=message.photo[-1].file_id,

                caption=caption + "Фото від клієнта 📸"

            )

        await message.answer(

            "Дякуємо за ваш відгук.\n"

            "Інформацію передано керівництву ресторану."

        )

async def main():

    await dp.start_polling(bot)

if __name__ == "__main__":

    asyncio.run(main())

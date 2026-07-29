from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import os
import sqlite3
import time


TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = -5179615999

bot = Bot(token=TOKEN)
dp = Dispatcher()


# ===== DATABASE =====

db = sqlite3.connect("reviews.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    user_id INTEGER PRIMARY KEY,
    date INTEGER
)
""")

db.commit()


def can_review(user_id):

    cursor.execute(
        "SELECT date FROM reviews WHERE user_id=?",
        (user_id,)
    )

    result = cursor.fetchone()

    if not result:
        return True

    last_date = result[0]

    if time.time() - last_date > 2592000:
        return True

    return False



def save_review(user_id):

    cursor.execute(
        "INSERT OR REPLACE INTO reviews VALUES (?,?)",
        (user_id, int(time.time()))
    )

    db.commit()



user_language = {}
waiting_feedback = set()
chosen_rating = {}



def languages():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇺🇦 Українська", callback_data="uk")],
            [InlineKeyboardButton(text="🇬🇧 English", callback_data="en")],
            [InlineKeyboardButton(text="🇱🇹 Lietuvių", callback_data="lt")]
        ]
    )



def ratings():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⭐1", callback_data="rating_1"),
                InlineKeyboardButton(text="⭐2", callback_data="rating_2"),
                InlineKeyboardButton(text="⭐3", callback_data="rating_3")
            ],
            [
                InlineKeyboardButton(text="⭐4", callback_data="rating_4"),
                InlineKeyboardButton(text="⭐5", callback_data="rating_5")
            ]
        ]
    )



@dp.message(Command("start"))
async def start(message: types.Message):

    if not can_review(message.from_user.id):

        await message.answer(
            "Ви вже залишали відгук 🤍\n\n"
            "Дякуємо, що обираєте Kyiv!"
        )
        return


    await message.answer(
        "👋 Вітаємо у ресторані Kyiv!\n\n"
        "Оберіть мову:",
        reply_markup=languages()
    )
    @dp.callback_query()
async def callback_handler(callback: types.CallbackQuery):

    user_id = callback.from_user.id


    # Вибір мови

    if callback.data in ["uk", "en", "lt"]:

        user_language[user_id] = callback.data

        texts = {
            "uk": "Чи сподобався вам ваш візит?\n\nОберіть оцінку ⭐️",
            "en": "Did you enjoy your visit?\n\nChoose your rating ⭐️",
            "lt": "Ar jums patiko jūsų apsilankymas?\n\nPasirinkite įvertinimą ⭐️"
        }


        await callback.message.answer(
            texts[callback.data],
            reply_markup=ratings()
        )


    # Вибір оцінки

    elif callback.data.startswith("rating_"):

        if not can_review(user_id):

            await callback.message.answer(
                "Ви вже залишали відгук 🤍\n"
                "Дякуємо!"
            )

            await callback.answer()
            return


        rating = callback.data.split("_")[1]

        chosen_rating[user_id] = rating


        lang = user_language.get(user_id, "uk")


        # Поганий відгук

        if rating in ["1", "2", "3"]:

            waiting_feedback.add(user_id)


            text = {
                "uk":
                "Нам шкода, що ваш візит не виправдав очікувань 😔\n\n"
                "Будь ласка, опишіть ситуацію.\n"
                "Ви також можете додати фото 📸",

                "en":
                "We are sorry your visit did not meet expectations 😔\n\n"
                "Please describe the situation.\n"
                "You can also add a photo 📸",

                "lt":
                "Apgailestaujame, kad jūsų apsilankymas neatitiko lūkesčių 😔\n\n"
                "Prašome aprašyti situaciją.\n"
                "Taip pat galite pridėti nuotrauką 📸"
            }


            await callback.message.answer(text[lang])


        # Хороший відгук

        else:

            save_review(user_id)


            text = {
                "uk":
                "Дякуємо за високу оцінку 🤍\n\n"
                "Будемо вдячні за ваш відгук у Google ⭐️",

                "en":
                "Thank you for your high rating 🤍\n\n"
                "We would appreciate your Google review ⭐️",

                "lt":
                "Dėkojame už aukštą įvertinimą 🤍\n\n"
                "Būtume dėkingi už atsiliepimą Google ⭐️"
            }


            button = {
                "uk": "⭐️ Залишити відгук Google",
                "en": "⭐️ Leave Google review",
                "lt": "⭐️ Palikti atsiliepimą Google"
            }


            google_button = InlineKeyboardMarkup(
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
                reply_markup=google_button
            )


    await callback.answer()



# Отримання тексту та фото після поганої оцінки

@dp.message()
async def receive_feedback(message: types.Message):

    user_id = message.from_user.id


    if user_id not in waiting_feedback:
        return


    waiting_feedback.remove(user_id)

    save_review(user_id)


    rating = chosen_rating.get(user_id, "?")


    caption = (
        "⚠️ Новий негативний відгук Kyiv\n\n"
        f"Оцінка: ⭐️{rating}\n"
        f"Клієнт: {message.from_user.full_name}\n\n"
    )


    if message.photo:

        await bot.send_photo(
            ADMIN_CHAT_ID,
            photo=message.photo[-1].file_id,
            caption=caption + (message.caption or "")
        )


    elif message.text:

        await bot.send_message(
            ADMIN_CHAT_ID,
            caption + message.text
        )


    await message.answer(
        "Дякуємо за ваш відгук 🙂\n\n"
        "Усі повідомлення автоматично передаються керівництву ресторану та уважно розглядаються."
    )



async def main():

    await dp.start_polling(bot)


if __name__== "__main__":
    asyncio.run(main())

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import os


TOKEN = os.getenv("BOT_TOKEN")

# ID групи адміністраторів
ADMIN_CHAT_ID = -5179615999


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
async def callback_handler(callback: types.CallbackQuery):

    user_id = callback.from_user.id


    # Вибір мови
    if callback.data in ["uk", "en", "lt"]:

        user_languages[user_id] = callback.data


        if callback.data == "uk":
            text = (
                "Чи сподобався вам візит?\n\n"
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
            text,
            reply_markup=keyboard
        )


    # Оцінка
    elif callback.data.startswith("rating_"):

        rating = callback.data.split("_")[1]

        lang = user_languages.get(user_id, "uk")


        if rating in ["1", "2", "3"]:

            await bot.send_message(
                ADMIN_CHAT_ID,
                f"⚠️ Новий відгук Kyiv\n\n"
                f"Оцінка клієнта: ⭐️{rating}"
            )


            if lang == "uk":
                answer = (
                    "Дякуємо за ваш відгук! 🙂\n\n"
                    "Усі повідомлення автоматично передаються "
                    "керівництву ресторану та уважно розглядаються."
                )

            elif lang == "en":
                answer = (
                    "Thank you for your feedback! 🙂\n\n"
                    "All messages are automatically forwarded "
                    "to the restaurant management and carefully reviewed."
                )

            else:
                answer = (
                    "Ačiū už jūsų atsiliepimą! 🙂\n\n"
                    "Visi pranešimai automatiškai perduodami "
                    "restorano vadovybei ir atidžiai peržiūrimi."
                )


            await callback.message.answer(answer)


        else:

            if lang == "uk":
                answer = (
                    "Дякуємо за високу оцінку 🤍\n\n"
                    "Будемо вдячні за ваш відгук у Google ⭐️"
                )
                button_text = "⭐️ Залишити відгук у Google"


            elif lang == "en":
                answer = (
                    "Thank you for your high rating 🤍\n\n"
                    "We would appreciate your Google review ⭐️"
                )
                button_text = "⭐️ Leave a Google review"


            else:
                answer = (
                    "Dėkojame už aukštą įvertinimą 🤍\n\n"
                    "Būtume dėkingi už jūsų atsiliepimą Google ⭐️"
                )
                button_text = "⭐️ Palikti atsiliepimą Google"


            google_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=button_text,
                            url="https://search.google.com/local/writereview?placeid=ChIJh2pRZtOV3UYR9-p0eIiDA2o"
                        )
                    ]
                ]
            )


            await callback.message.answer(
                answer,
                reply_markup=google_keyboard
            )


    await callback.answer()
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
                "Дякуємо за ваш відгук! 🙂\n\n"
                "Усі повідомлення автоматично передаються "
                "керівництву ресторану та уважно розглядаються."
            )


        else:

    print("ВИСОКА ОЦІНКА")

    google_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⭐️ Залишити відгук у Google",
                    url="https://search.google.com/local/writereview?placeid=ChIJh2pRZtOV3UYR9-p0eIiDA2o"
                )
            ]
        ]
    )

    await callback.message.answer(
        "Дякуємо за високу оцінку 🤍\n\n"
        "Будемо вдячні за ваш відгук у Google ⭐️",
        reply_markup=google_keyboard
    )

    await callback.answer()



async def main():

    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())


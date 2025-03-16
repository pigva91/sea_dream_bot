import logging

from keyboards import main_kb
from registrate_router import reg_1, reg_router
from call_router import callback_router
from config import settings
from sqlbd import *

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

dp = Dispatcher()
bot = Bot(token=settings.TOKEN.get_secret_value())


@dp.message(Command("start"))
async def start(message: Message, state: FSMContext):
    """Приветствует пользователя и проверяет, зарегистрирован ли он в базе данных. Если да, отправляет главное меню.
    Если нет, предлагает заполнить регистрационную форму."""
    user_id = message.from_user.id
    logging.info(f"UserID={user_id}, UserNick={message.from_user.username}, UserFullName={message.from_user.full_name}")
    count = check_id(user_id)

    if count > 0:
        await message.answer(text="Добрый день, рад Вас снова видеть\nВыберите действие ⤵️", reply_markup=main_kb)
    else:
        insert_id(user_id)

        # Добавить название компании
        text = ("Приветствую, будущий обладатель дома мечты у моря 🤝\n\nЯ бот компании 'НАЗВАНИЕ КОМПАНИИ', "
                "оставь информацию мне и я передам ее лучшему брокеру компании и он станет твоим проводником на "
                "главном курорте страны 🏝️")
        await message.answer(text=text)
        await reg_1(message, state)


@dp.message(Command("site"))
async def site(message: Message):
    """Отправляет ссылку на сайт компании."""
    # Добавить ссылку на сайт компании
    await message.answer(text="Вот ссылка на наш сайт 👇\n'ССЫЛКА НА САЙТ'")


@dp.message(Command("chat"))
async def site(message: Message):
    """Отправляет ссылку на чат компании."""
    # Добавить ссылку на чат компании
    await message.answer(text="Вот ссылка на наш чат 👇\n'ССЫЛКА НА ТГ-ЧАТ'")


@dp.message(Command("application"))
async def site(message: Message, state: FSMContext):
    """Предлагает заполнить регистрационную форму."""
    await reg_1(message, state)


async def main():
    """Запускает бота."""
    try:
        create_table()
        dp.include_routers(reg_router, callback_router)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as err:
        logging.error(err)


if __name__ == "__main__":
    try:
        logging.basicConfig(filename="py_log.log", level=logging.INFO,
                            format=" %(asctime)s - %(""levelname)s - %(message)s")
        asyncio.run(main())
    except KeyboardInterrupt as err:
        logging.error("BOT OFF")

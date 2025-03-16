from aiogram.fsm.context import FSMContext
from aiogram.types import  CallbackQuery, Message
from aiogram import Router, F
from registrate_router import reg_1
from sqlbd import *
from keyboards import *


callback_router = Router()


@callback_router.callback_query(F.data == "Заявка")
async def application(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await reg_1(callback.message, state)


@callback_router.callback_query(F.data == "Главная")
async def start(callback: Message, state: FSMContext):
    await callback.answer()
    user_id = callback.message.from_user.id
    count = check_id(user_id)

    if  count > 0:
        await callback.message.answer(
            text="Добрый день, рад Вас снова видеть\nВыберите действие ⤵️",
            reply_markup=main_kb
        )
    else:
        insert_id(user_id)

        # Добавить название компании
        text = ("Приветствую, будущий обладатель дома мечты у моря 🤝\n\nЯ бот компании 'НАЗВАНИЕ КОМПАНИИ', "
                "оставь информацию мне и я передам ее лучшему брокеру компании и он станет твоим проводником на "
                "главном курорте страны 🏝️")
        await callback.message.answer(text=text)

        await reg_1(callback.message, state)

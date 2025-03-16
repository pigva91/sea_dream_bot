import logging
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove
from aiogram import Router
import re
from request import req
from keyboards import reg_kb, phone_kb, type_of_funds_kb, types_kb, budget_kb


class Reg(StatesGroup):
    name = State()
    number = State()
    city = State()
    type = State()
    budget = State()
    type_of_funds = State()
    detail = State()
    district = State()


reg_router = Router()


async def reg_1(message: Message, state: FSMContext):
    """Регистрация пользователя"""
    try:
        await message.delete()
        await state.set_state(Reg.name)
        await message.answer("Вам нужно ответить на несколько вопросов 📃")
        await message.answer("Как вас зовут? Введите фамилию, имя и отчество через пробел ✍️")
    except Exception as err: 
        logging.error(f"Ошибка в reg_1: {err}")


@reg_router.message(Reg.name)
async def reg_2(message: Message, state: FSMContext):
    """Регистрация ФИО"""
    try:
        pattern = r'^[А-ЯЁа-яё]+\s[А-ЯЁа-яё]+\s[А-ЯЁа-яё]+$'
        if not re.match(pattern, message.text):
            await message.reply(
                "ФИО должно состоять только из букв. Пожалуйста, введите фамилию, имя и отчество через пробел.")
            return
        await state.update_data(name=message.text.title())
        await state.set_state(Reg.number)
        await message.answer("Введите ваш номер телефона 📞", reply_markup=phone_kb)
    except Exception as err:
        logging.error(f"Ошибка в reg_2: {err}")
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте еще раз.")


@reg_router.message(Reg.number)
async def reg_3(message: Message, state: FSMContext):
    """Регистрация номера"""
    try:
        pattern = r'^(\+7|7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$'
        if message.contact:
            # Если номер отправлен через кнопку "Поделиться контактом"
            phone_number = message.contact.phone_number
            if not re.match(pattern, phone_number):
                await message.reply(
                    "Пожалуйста, введите номер телефона в формате +7XXXXXXXXXX, 7XXXXXXXXXX или 8XXXXXXXXXX "
                    "или нажмите на кнопку ниже.", reply_markup=phone_kb)
                return
        else:
            # Если номер введен вручную
            if not re.match(pattern, message.text):
                await message.reply(
                    "Пожалуйста, введите номер телефона в формате +7XXXXXXXXXX, 7XXXXXXXXXX или 8XXXXXXXXXX "
                    "или нажмите на кнопку ниже.", reply_markup=phone_kb
                )
                return
            phone_number = message.text
        await state.update_data(number=phone_number)
        await state.set_state(Reg.city)
        await message.answer("Из какого вы города 🌆", reply_markup=ReplyKeyboardRemove())
    except Exception as err:
        logging.error(f"Ошибка в reg_3: {err}")
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте еще раз.", reply_markup=phone_kb)


@reg_router.message(Reg.city)
async def reg_4(message: Message, state: FSMContext):
    """Регистрация города"""
    try:
        pattern = r'^[А-ЯЁа-яё\s-]+$'
        if not re.match(pattern, message.text):
            await message.reply("Пожалуйста, введите корректное название города.")
            return
        await state.update_data(city=message.text.title())
        await state.set_state(Reg.type)
        await message.answer("Что вы хотите приобрести? 🏡", reply_markup=types_kb)
    except Exception as err:
        logging.error(f"Ошибка в reg_4: {err}")
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте еще раз.")


@reg_router.message(Reg.type)
async def reg_5(message: Message, state: FSMContext):
    """Регистрация типа объекта"""
    try:
        if message.text.lower() not in [
            "дом", "земельный участок", "участок",
            "квартира", "апартаменты", "апарты", "другое"
        ]:
            await message.reply(
                "Пожалуйста, выберите тип объекта из предложенных вариантов:",
                reply_markup=types_kb)
            return
        await state.update_data(type=message.text.title())
        print(message.text.title())
        await state.set_state(Reg.budget)
        await message.answer("Какой бюджет закладываете на покупку? 💵 (в млн. руб.)", reply_markup=budget_kb)
    except Exception as err:
        logging.error(f"Ошибка в reg_5: {err}")
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте еще раз.", reply_markup=types_kb)


@reg_router.message(Reg.budget)
async def reg_6(message: Message, state: FSMContext):
    """Регистрация бюджета"""
    try:
        if message.text in [
            "5 - 10", "10 - 15", "15 - 20", "20 - 25", "25 - 30", "30 - 40", "40 - 50", "Свыше 50"
        ]:
            await state.update_data(budget=message.text.title())
        else:
            try:
                user_budget = int(message.text)
                if 5 <= user_budget <= 300:
                    await state.update_data(budget=user_budget)
                else:
                    await message.reply(
                        "Пожалуйста, выберите бюджет из предложенных вариантов:",
                        reply_markup=budget_kb
                    )
                    return
            except ValueError:
                await message.reply(
                    "Пожалуйста, введите число или выберите из предложенных вариантов.",
                    reply_markup=budget_kb
                )
                return
        await state.set_state(Reg.type_of_funds)
        await message.answer("Ипотека или личные средства?", reply_markup=type_of_funds_kb)
    except Exception as err:
        logging.error(f"Ошибка в reg_6: {err}")
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте еще раз.", reply_markup=budget_kb)


@reg_router.message(Reg.type_of_funds)
async def reg_7(message: Message, state: FSMContext):
    """Регистрация типа средств"""
    try:
        if message.text.lower() not in ["ипотека", "личные средства", "личные", "нал", "наличка", "другое"]:
            await message.reply("Пожалуйста, введите корректный тип средств.", reply_markup=type_of_funds_kb)
            return
        await state.update_data(type_of_funds=message.text.title())
        await state.set_state(Reg.detail)
        await message.answer(
            "Опишите, что важно для покупки и укажите все детали ✍️",
            reply_markup=ReplyKeyboardRemove()
        )
    except Exception as err:
        logging.error(f"Ошибка в reg_7: {err}")
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте еще раз.", reply_markup=type_of_funds_kb)


@reg_router.message(Reg.detail)
async def reg_8(message: Message, state: FSMContext):
    """Регистрация дополнительных деталей"""
    try:
        if message.photo or message.document:
            await message.reply("Пожалуйста, введите корректные детали.")
            return
        await state.update_data(detail=message.text.lower())
        await state.set_state(Reg.district)
        await message.answer("Какой район Сочи рассматриваете?")
    except Exception as err:
        logging.error(f"Ошибка в reg_8: {err}")
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте еще раз.")


@reg_router.message(Reg.district)
async def reg_9(message: Message, state: FSMContext):
    """Регистрация предпочтения района"""
    try:
        if any ([message.text.isdigit(), message.photo, message.document]):
            await message.reply("Пожалуйста, введите корректное название района.")
            return
        await state.update_data(district=message.text.title())
        data = await state.get_data()
        path_video = '/root/bots/deploy_bot/video.mp4'
        await message.answer_video_note(video_note=FSInputFile(path=path_video))
        await message.answer(
            "Спасибо за доверие!\nЯ уже ищу лучшего брокера для работы с вами 👌",
            reply_markup=reg_kb
        )

        req(data["name"],
            data["number"],
            data["city"],
            data["type"],
            data["budget"],
            data["type_of_funds"],
            data["detail"],
            data["district"])
        await state.clear()

    except Exception as err:
        logging.error(f"Ошибка в reg_9: {err}")

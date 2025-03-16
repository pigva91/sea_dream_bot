from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


# Кнопки главного меню
# Добавить ссылку на сайт компании и ссылку на чат телеграм
main_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Связаться с менеджером", url='ССЫЛКА НА ТГ_ЧАТ')],
    [InlineKeyboardButton(text="Оставить еще одну заявку", callback_data="Заявка")],
    [InlineKeyboardButton(text="Перейти на сайт компании", url='ССЫЛКА НА САЙТ')]
]
)

# Кнопка для возврата на главную страницу
reg_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="На главную", callback_data="Главная")]
]
)

# Кнопка для отправки номера телефона
phone_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱Поделиться контактом", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Кнопки для выбора типа оплаты
type_of_funds_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Ипотека"),
            KeyboardButton(text="Личные средства")
        ],
        [
            KeyboardButton(text="Другое")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Кнопки для выбора типа недвижимости
types_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Дом"),
            KeyboardButton(text="Земельный участок"),
        ],
        [
            KeyboardButton(text="Квартира"),
            KeyboardButton(text="Апартаменты"),
        ],
        [KeyboardButton(text="Другое")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Кнопки для выбора бюджета
budget_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="5 - 10"),
            KeyboardButton(text="10 - 15"),
            KeyboardButton(text="15 - 20"),
        ],
        [
            KeyboardButton(text="20 - 25"),
            KeyboardButton(text="25 - 30"),
            KeyboardButton(text="30 - 40"),
        ],
        [
            KeyboardButton(text="40 - 50"),
            KeyboardButton(text="Свыше 50")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

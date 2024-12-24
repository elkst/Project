from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from callback_factory.callback_factory import ScheduleCallbackFactory, MainMenuCallbackFactory


# Главное меню
def get_main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="ℹ️ Информация",
            callback_data=MainMenuCallbackFactory(action="information").pack()
        ),
        InlineKeyboardButton(
            text="📝 Связаться с администратором",
            callback_data=MainMenuCallbackFactory(action="contact_admin").pack()
        ),
        InlineKeyboardButton(
            text="📅 Расписание",
            callback_data=MainMenuCallbackFactory(action="schedule").pack()
        ),
        InlineKeyboardButton(
            text="💳 Поддержать",
            callback_data=MainMenuCallbackFactory(action="support").pack()
        ),
        width=1  # Устанавливаем ширину строки (по одной кнопке в строке)
    )
    return builder.as_markup()

def get_group_selection_keyboard():
    groups = [
        {"name": "ИВТ-201", "id": 1},
        {"name": "ПРИ-201", "id": 2},
        {"name": "ПИ-201", "id": 3},
        {"name": "ИСТ-201", "id": 4}
    ]
    builder = InlineKeyboardBuilder()
    for group in groups:
        builder.add(
            InlineKeyboardButton(
                text=f"{group['name']}",
                callback_data=ScheduleCallbackFactory(action=f"group_{group['name']}").pack()
            )
        )
    return builder.as_markup()

# Клавиатура для выбора дней недели
def get_days_keyboard():
    days = [
        {"name": "Пн", "id": 1},
        {"name": "Вт", "id": 2},
        {"name": "Ср", "id": 3},
        {"name": "Чт", "id": 4},
        {"name": "Пт", "id": 5},
        {"name": "Сб", "id": 6},
        {"name": "Все дни", "id": 7}
    ]
    builder = InlineKeyboardBuilder()
    for day in days:
        builder.add(
            InlineKeyboardButton(
                text=day["name"],
                callback_data=f"day_{day['id']}"
            )
        )
    return builder.as_markup()


from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from callback_factory.callback_factory import MainMenuCallbackFactory

# Создаём клавиатуру
main_menu_kb_builder = InlineKeyboardBuilder()

# Добавляем кнопки
main_menu_kb_builder.row(
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
    width=2  # Устанавливаем ширину строки
)

# Получение готовой клавиатуры
main_menu_inline_kb = main_menu_kb_builder.as_markup()

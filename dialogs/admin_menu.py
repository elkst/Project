from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button, Back
from aiogram_dialog.widgets.text import Const, Format
from handlers.admin_handlers import show_users
from states.fsm import AdminDialogStates

# Главное меню админ-панели
admin_menu = Window(
    Const("🔧 Админ-панель"),
    Button(
        Const("📋 Пользователи"),
        id="users_btn",
        on_click=lambda c, widget, manager: manager.switch_to(AdminDialogStates.users)  # Переход к окну пользователей
    ),

    state=AdminDialogStates.admin_menu,
)

# Окно списка пользователей
users = Window(
    Format(
        "📋 Список пользователей:\n\n"
        "{users_text}"  # Место для динамического текста
    ),
    Back(Const("Назад")),
    state=AdminDialogStates.users,
    getter=show_users  # Связь с функцией получения данных
)

# Диалог
admin_dialog = Dialog(
    admin_menu,
    users
)

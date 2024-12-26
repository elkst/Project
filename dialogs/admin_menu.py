from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Back
from aiogram_dialog.widgets.text import Const, Format
from handlers.admin_handlers import show_users
from states.fsm import AdminDialogStates
from aiogram_dialog import DialogManager


async def clear_exit_message(dialog_manager: DialogManager):
    dialog_manager.dialog_data.clear()


# Главное меню админ-панели
admin_menu = Window(
    Const("🔧 Админ-панель"),
    Button(
        Const("📋 Пользователи"),
        id="users_btn",
        on_click=lambda c, widget, manager: manager.switch_to(AdminDialogStates.users)
    ),
    Button(
        Const("🚪 Выход"),
        id="exit_btn",
        on_click=lambda c, widget, manager: manager.switch_to(AdminDialogStates.confirm_exit)
    ),
    state=AdminDialogStates.admin_menu,
)

# Окно списка пользователей
users = Window(
    Format("📋 Список пользователей:\n\n{users_text}"),
    Back(Const("🔙 Назад")),
    state=AdminDialogStates.users,
    getter=show_users
)

# Окно подтверждения выхода
confirm_exit = Window(
    Const("Вы действительно хотите выйти из админ-панели?"),
    Button(
        Const("Да"),
        id="confirm_exit_yes",
        on_click=lambda c, widget, manager: manager.switch_to(AdminDialogStates.exit_message)
    ),
    Button(
        Const("Нет"),
        id="confirm_exit_no",
        on_click=lambda c, widget, manager: manager.switch_to(AdminDialogStates.admin_menu)
    ),
    state=AdminDialogStates.confirm_exit,
)

# Окно с сообщением "Вы вышли из панели"
exit_message = Window(
    Format("Вы вышли из панели"),
    Button(Const("Ок"), id="back", on_click=lambda c, widget, manager: manager.done()),
    state=AdminDialogStates.exit_message,
)

# Диалог
admin_dialog = Dialog(
    admin_menu,
    users,
    confirm_exit,
    exit_message
)

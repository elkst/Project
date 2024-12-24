from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram_dialog import DialogManager, StartMode

from filters.is_admin import IsAdminFilter
from database.methods.methods import get_all_users
from states.fsm import AdminDialogStates

admin_router = Router()

async def show_users(dialog_manager: DialogManager, **kwargs) -> dict:
    users = get_all_users()  # Получаем пользователей из базы данных

    # Формируем текст для отображения списка пользователей
    users_text = "\n\n".join(
        f"👤 Username: {user['username'] or '—'}\n"
        f" ├ ID Telegram: {user['id_telegram']}"
        for user in users
    )

    return {"users_text": users_text}


# вызов диалога админа
@admin_router.message(Command("admin"), IsAdminFilter)
async def admin_panel(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(AdminDialogStates.admin_menu, mode=StartMode.RESET_STACK)

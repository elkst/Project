import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from handlers.payment_handlers import payment_router  # Импортируем роутер

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from handlers.base_commands import user_router
from handlers.admin_handlers import admin_router
from dialogs.admin_menu import admin_dialog
from config_data.config import load_config, Config  # Импорт функции и класса для конфигурации
from filters.is_admin import IsAdminFilter

# Загрузка конфигурации из файла .env
config: Config = load_config()  # Создаем объект конфигурации

# Создание экземпляра Telegram-бота
bot = Bot(token=config.tg_bot.token)

# Инициализация диспетчера
dp = Dispatcher(storage=MemoryStorage())

async def main() -> None:
    # Настройка aiogram_dialog
    setup_dialogs(dp)  # Подключение системы диалогов

    # Регистрация диалогов
    dp.include_router(admin_dialog)  # Диалог админ-панели

    # Регистрация роутеров
    dp.include_router(user_router)  # Роутер для пользователей
    dp.include_router(admin_router)  # Роутер для администраторов
    dp.include_router(payment_router)  # Роутер для обработки платежей
    # Применение фильтра для сообщений от администраторов
    admin_ids = config.tg_bot.admin_ids  # Получение списка ID администраторов из конфигурации
    admin_router.message.filter(IsAdminFilter(admin_ids=admin_ids))  # Фильтр для администраторских сообщений

    # Запуск поллинга
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот остановлен пользователем.")

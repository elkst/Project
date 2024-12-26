from aiogram import BaseMiddleware
from aiogram.types import Update
import sqlite3


class AdminMiddleware(BaseMiddleware):
    def __init__(self, db_path, bot_id):
        super().__init__()
        self.db_path = db_path
        self.bot_id = bot_id

    async def __call__(self, handler, event: Update, data: dict):
        # Создаем подключение к базе данных
        conn = sqlite3.connect(self.db_path)
        data["dialog_manager"].middleware_data.update({
            "db_connection": conn,
            "bot_id": self.bot_id
        })

        # Вызываем следующий обработчик
        result = await handler(event, data)

        # Закрываем подключение после обработки запроса
        conn.close()

        return result

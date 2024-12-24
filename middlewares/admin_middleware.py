from aiogram import BaseMiddleware
from aiogram.types import Update

class AdminMiddleware(BaseMiddleware):
    def __init__(self, db_pool, bot_id):
        self.db_pool = db_pool
        self.bot_id = bot_id

    async def __call__(self, handler, event: Update, data: dict):
        data["dialog_manager"].middleware_data.update({
            "db_pool": self.db_pool,
            "bot_id": self.bot_id
        })
        return await handler(event, data)

from aiogram.filters import BaseFilter  # Импортируем базовый класс фильтра из библиотеки aiogram
from aiogram.types import Message  # Импортируем тип Message для работы с сообщениями


class IsAdminFilter(BaseFilter):  # Определяем новый фильтр, наследующий от BaseFilter
    def __init__(self, admin_ids: list[int]):  # Конструктор класса, принимает список идентификаторов администраторов
        self.admin_ids = admin_ids  # Сохраняем список идентификаторов в атрибуте экземпляра

    async def __call__(self,
                       message: Message) -> bool:  # Асинхронный метод, который будет вызываться при проверке фильтра
        is_admin = message.from_user.id in self.admin_ids  # Проверяем, является ли отправитель сообщения администратором
        return is_admin  # Возвращаем True, если пользователь является администратором, иначе False

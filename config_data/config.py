from dataclasses import dataclass  # Для создания структур данных
from environs import Env  # Удобная работа с переменными окружения


@dataclass
class TgBot:
    token: str  # Токен для взаимодействия с Telegram Bot API
    admin_ids: list[int]  # Список ID администраторов


# Главный класс конфигурации, объединяющий все настройки
@dataclass
class Config:
    tg_bot: TgBot  # Настройки Telegram-бота


# Функция загрузки конфигурации из файла .env
def load_config(path: str | None = None) -> Config:
    """
    Загружает конфигурацию из файла .env.

    :param path: Путь до файла .env. Если None, используется файл по умолчанию.
    :return: Объект Config, содержащий все настройки.
    """
    env = Env()  # Создаем экземпляр для работы с переменными окружения
    env.read_env(path)  # Читаем переменные окружения из файла .env

    return Config(
        tg_bot=TgBot(
            token=env("BOT_TOKEN"),  # Считываем токен бота
            admin_ids=[int(admin_id.strip()) for admin_id in env.list("ADMIN_IDS")]
            # Преобразуем список ID администраторов в целые числа
        )
    )

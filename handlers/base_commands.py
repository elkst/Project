from aiogram import Router, Bot  # Импортируем Router и Bot из библиотеки aiogram
from aiogram.filters import Command, CommandStart, StateFilter  # Импортируем фильтры для обработки команд и состояний
from aiogram.fsm.context import FSMContext  # Импортируем контекст для работы с состояниями
from aiogram.types import Message, CallbackQuery  # Импортируем типы сообщений и колбек-запросов

from database.methods.methods import register_user, get_group_schedule  # Импортируем функции для работы с базой данных
from keyboards.keyboards import get_group_selection_keyboard, get_days_keyboard, \
    get_main_menu_keyboard  # Импортируем функции для создания клавиатур
from lexicon.lexicon import LEXICON_RU  # Импортируем словарь с текстами на русском языке
from states.fsm import ScheduleState, ReportState  # Импортируем состояния для управления логикой бота
from database.misc import create_text_schedule  # Импортируем функцию для создания текстового расписания

import os  # Импортируем модуль os для работы с окружением
from dotenv import load_dotenv  # Импортируем функцию для загрузки переменных окружения из .env файла

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем идентификаторы администраторов из переменной окружения и преобразуем их в список целых чисел
admin_ids = list(map(int, os.getenv("ADMIN_IDS", "").split(',')))

user_router = Router(name=__name__)  # Создаем новый роутер для обработки пользовательских команд


@user_router.message(CommandStart())  # Обработчик команды /start
async def command_start_handler(message: Message) -> None:
    telegram_id = message.from_user.id  # Получаем ID пользователя из сообщения
    first_name = message.from_user.first_name  # Получаем имя пользователя

    # Регистрируем пользователя в базе данных
    register_user(telegram_id, first_name)

    # Отправляем приветственное сообщение с основным меню
    await message.answer(
        text=LEXICON_RU['/start'],  # Текст приветствия из словаря
        reply_markup=get_main_menu_keyboard(),  # Клавиатура основного меню
    )


# Обработчик нажатия кнопки "Расписание"
@user_router.callback_query(lambda c: c.data.startswith('main_menu:schedule'))
async def handle_schedule_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()  # Уведомляем Telegram о том, что колбек обработан
    await callback.message.edit_text("Выберите группу:",
                                     reply_markup=get_group_selection_keyboard())  # Запрашиваем выбор группы
    await state.set_state(ScheduleState.select_group)  # Устанавливаем состояние выбора группы


# Обработчик выбора группы
@user_router.callback_query(lambda c: c.data.startswith("schedule:group_"))
async def handle_group_selection(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()  # Уведомляем Telegram о том, что колбек обработан
    group_name = callback.data.replace("schedule:group_", "")  # Извлекаем название группы из callback_data
    schedule = get_group_schedule(group_name)  # Получаем расписание для выбранной группы

    if not schedule:  # Если расписание не найдено
        await callback.message.edit_text("Расписание для этой группы не найдено.")  # Информируем пользователя
        return

    await state.update_data(group_name=group_name)  # Сохраняем название группы в состоянии
    await callback.message.edit_text("Выберите день недели:",
                                     reply_markup=get_days_keyboard())  # Запрашиваем выбор дня недели
    await state.set_state(ScheduleState.select_day)  # Устанавливаем состояние выбора дня


# Обработчик выбора дня недели
@user_router.callback_query(StateFilter(ScheduleState.select_day))
async def handle_select_day(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()  # Уведомляем Telegram о том, что колбек обработан

    user_data = await state.get_data()  # Получаем данные состояния пользователя
    group_name = user_data["group_name"]  # Извлекаем название группы

    day_id = callback.data.replace("day_", "")  # Получаем id дня недели из callback_data

    if day_id.isdigit():  # Проверяем, является ли day_id числом
        day_id = int(day_id)  # Преобразуем в число
    else:
        await callback.answer("Ошибка: Неверный формат данных.", show_alert=True)  # Сообщаем об ошибке формата данных
        return

    day_of_week = None if day_id == 7 else day_id  # Если выбран пункт "Все дни", передаем None

    schedule = get_group_schedule(group_name, day_of_week)  # Получаем расписание из базы данных

    if not schedule:  # Если расписание не найдено для выбранного дня
        await callback.message.edit_text("Расписание не найдено для этого дня.")  # Информируем пользователя
        return

    if day_id == 7:  # Если выбраны все дни, выводим расписание для всех дней
        text = "\n\n".join(
            create_text_schedule(schedule, day) for day in range(1, 7)
            # Генерируем текст расписания для каждого дня недели
        )
    else:
        text = create_text_schedule(schedule, day_of_week)  # Генерируем текст расписания для одного дня

    await callback.message.edit_text(text)  # Изменяем текст сообщения на полученное расписание
    await state.clear()  # Очищаем состояние пользователя


# Обработчик команды /report
@user_router.message(Command('report'))
async def command_report_handler(message: Message, state: FSMContext) -> None:
    await message.answer('Введите ваше сообщение:')  # Запрашиваем сообщение от пользователя
    await state.set_state(ReportState.report_message)  # Устанавливаем состояние для обработки сообщения отчета


# Обработчик сообщения отчета
@user_router.message(ReportState.report_message)
async def process_report_message(message: Message, state: FSMContext, bot: Bot) -> None:
    for tg_id in admin_ids:
        await bot.send_message(tg_id, f'Пришло сообщение: {message.text}')  # Отправляем сообщение всем администраторам

    await message.answer("Ваш отчет отправлен администраторам.")  # Подтверждение отправки отчета пользователю.

    await state.clear()  # Очищаем состояние после отправки отчета


# Обработчик нажатия кнопки "Информация"
@user_router.callback_query(lambda c: c.data.startswith('main_menu:information'))
async def handle_information_callback(callback: CallbackQuery) -> None:
    await callback.answer()
    info_text = (
        "Это бот для получения расписания.\n"
        "Вы можете выбрать группу и день недели, чтобы получить актуальное расписание."
    )
    await callback.message.answer(info_text)  # Отправляем информацию пользователю


# Обработчик нажатия кнопки "Связаться с администратором"
@user_router.callback_query(lambda c: c.data.startswith('main_menu:contact_admin'))
async def handle_contact_admin_callback(callback: CallbackQuery) -> None:
    await callback.answer()
    admin_contact = "Вы можете связаться с администратором, написав ему в личные сообщения: https://t.me/olkdz"
    await callback.message.answer(admin_contact)  # Отправляем контактную информацию администратора пользователю

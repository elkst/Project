from aiogram.fsm.state import StatesGroup, State  # Импортируем классы для работы с состояниями из aiogram

# Определяем группу состояний для выбора дня
class DayState(StatesGroup):
    day = State()  # Состояние для выбора дня

# Определяем группу состояний для обработки сообщений отчета
class ReportState(StatesGroup):
    report_message = State()  # Состояние для ожидания сообщения отчета

# Определяем группу состояний для работы с расписанием
class ScheduleState(StatesGroup):
    select_group = State()  # Состояние для выбора группы
    select_day = State()    # Состояние для выбора дня недели

# Определяем группы состояний для админ-панели
class AdminDialogStates(StatesGroup):
    admin_menu = State()  # Состояние для отображения меню администратора
    stats = State()       # Состояние для просмотра статистики
    users = State()      # Состояние для управления пользователями

# Определяем группу состояний для поддержки
class SupportState(StatesGroup):
    waiting_for_payment = State()  # Состояние ожидания подтверждения оплаты

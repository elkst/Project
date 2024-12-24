# Функция для генерации текста расписания
def create_text_schedule(schedule, day_of_week):
    """
    Формирование текста расписания для одного дня.
    """
    text = f"Расписание на {day_of_week}:\n\n"
    for item in schedule:
        text += (f"Предмет: {item[3]}\n"
                 f"Время: {item[4]} - {item[5]}\n"
                 f"Преподаватель: {item[6]}\n"
                 f"Корпус: {item[7]}\n"
                 f"Аудитория: {item[8]}\n\n")
    return text

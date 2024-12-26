from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Format
from states.fsm import BuildingDialogStates


async def on_back_button_click(dialog_manager):
    await dialog_manager.done(result="back_to_start")


# Окно для корпуса 1
building_1 = Window(
    StaticMedia(
        path="assets/k1.jpg",  # Относительный путь к изображению
        type="photo"  # Тип медиа
    ),
    Format(
        "🏢 Первый корпус\n\n"
        "[Открыть карту](https://yandex.ru/maps/org/bryanskiy_gosudarstvenny_inzhenerno_tekhnologicheskiy_universitet/1054202859/?ll=34.358364%2C53.246767&mode=search&sll=34.296640%2C53.263004&sspn=0.122566%2C0.043435&text=%D0%91%D0%B3%D0%B8%D1%82%D1%83&utm_source=share&z=15)"
    ),
    Button(Format("🔙 Назад"), id="back", on_click=lambda c, w, m: m.switch_to(BuildingDialogStates.main)),
    state=BuildingDialogStates.building_1
)

# Окно для корпуса 2
building_2 = Window(
    StaticMedia(
        path="assets/k2.jpg",  # Относительный путь к изображению
        type="photo"  # Тип медиа
    ),
    Format(
        "🏢 Второй корпус\n\n"
        "[Открыть карту](https://yandex.ru/maps/org/bryanskiy_gosudarstvenny_inzhenerno_tekhnologicheskiy_universitet_korpus_2a/1139844625/?ll=34.358364%2C53.246767&mode=search&sll=34.296640%2C53.263004&sspn=0.122566%2C0.043435&text=%D0%91%D0%B3%D0%B8%D1%82%D1%83&utm_source=share&z=15)"
    ),
    Button(Format("🔙 Назад"), id="back", on_click=lambda c, w, m: m.switch_to(BuildingDialogStates.main)),
    state=BuildingDialogStates.building_2
)

# Главное меню выбора корпусов
building_menu = Window(
    Format("Выберите корпус:"),
    Button(Format("🏢 Первый корпус"), id="building_1",
           on_click=lambda c, w, m: m.switch_to(BuildingDialogStates.building_1)),
    Button(Format("🏢 Второй корпус"), id="building_2",
           on_click=lambda c, w, m: m.switch_to(BuildingDialogStates.building_2)),
    Button(
        Format("🔙 Назад"),
        id="back",
        on_click=lambda c, w, m: m.done(result="back_to_start")  # Передаем результат при завершении диалога
    ),

    state=BuildingDialogStates.main
)

# Диалог
building_dialog = Dialog(
    building_menu,
    building_1,
    building_2
)

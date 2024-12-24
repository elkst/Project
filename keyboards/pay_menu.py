from aiogram.utils.keyboard import InlineKeyboardBuilder

pay_btn_bldr = InlineKeyboardBuilder()
pay_btn_bldr.button(text="Оплатить", callback_data="pay_premium")

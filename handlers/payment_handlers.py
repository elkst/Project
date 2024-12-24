from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, ContentType, LabeledPrice
from keyboards.pay_menu import pay_btn_bldr

payment_router = Router()

# Обработка callback-запроса на поддержку
@payment_router.callback_query(lambda c: c.data.startswith('main_menu:support'))
async def send_invoice(callback: CallbackQuery, bot: Bot):
    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title="Поддержка разработчика",
        description="Вы можете поддержать разработчика, оплатив указанную сумму.",
        payload="support_project",
        provider_token="1744374395:TEST:366df06a16c83c18d9bf",  # Токен провайдера
        currency="RUB",
        prices=[
            LabeledPrice(label="Поддержка проекта", amount=500_00)
        ],
        max_tip_amount=10000,
        suggested_tip_amounts=[1000, 2000, 5000],
        start_parameter="support",
        need_name=False,
        need_phone_number=False,
        need_email=False,
        need_shipping_address=False,
    )
    await callback.answer()

# Обработка предоплаты
@payment_router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# Обработка успешной оплаты
@payment_router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: Message):
    total_amount = message.successful_payment.total_amount / 100
    await message.answer(
        text=f"Спасибо за поддержку разработчика! Вы оплатили {total_amount} {message.successful_payment.currency}."
    )

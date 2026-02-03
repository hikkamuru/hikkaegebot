"""User payment confirmation handlers."""
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from keyboards import (
    get_payment_keyboard,
    get_back_to_menu_keyboard,
    get_admin_request_keyboard,
    UserPaymentCallback,
)
from data import get_pending_request, decline_pending_request, get_card_by_id
from config import ADMIN_ID

router = Router()


@router.callback_query(UserPaymentCallback.filter(F.action == "paid"))
async def user_paid(callback: CallbackQuery, callback_data: UserPaymentCallback, bot: Bot) -> None:
    """User confirms payment - send request to admin."""
    req = get_pending_request(callback_data.req_id)
    if not req:
        await callback.answer("Заявка не найдена", show_alert=True)
        return

    card = get_card_by_id(req.card_id)

    # Update user message
    user_text = """
<b>✅ Оплата отмечена</b>

Спасибо! Администратор проверит оплату и подтвердит вашу подписку.

<i>Ожидайте подтверждения...</i>
"""
    try:
        await callback.message.edit_text(user_text, parse_mode="HTML", reply_markup=get_back_to_menu_keyboard())
    except Exception:
        await callback.message.edit_caption(caption=user_text, parse_mode="HTML", reply_markup=get_back_to_menu_keyboard())

    await callback.answer("Отлично!")

    # Send request to admin
    if ADMIN_ID:
        admin_text = f"""
<b>🆕 Новая заявка на подписку</b>

━━━━━━━━━━━━━━━━━━━━━━
<b>👤 Клиент:</b> {req.full_name}
<b>📞 Телефон:</b> {req.phone}
<b>🔗 Username:</b> @{req.username or 'нет'}
<b>🆔 ID:</b> <code>{req.user_id}</code>
━━━━━━━━━━━━━━━━━━━━━━

<b>📦 Подписка:</b> {req.card_name}
<b>💰 Сумма:</b> <b>{req.price:,} ₽</b>

<i>Оплата произведена. Подтвердите:</i>
"""
        try:
            if card:
                await bot.send_photo(
                    chat_id=ADMIN_ID,
                    photo=card.image_url,
                    caption=admin_text,
                    reply_markup=get_admin_request_keyboard(callback_data.req_id),
                )
            else:
                await bot.send_message(
                    chat_id=ADMIN_ID,
                    text=admin_text,
                    reply_markup=get_admin_request_keyboard(callback_data.req_id),
                )
        except Exception:
            await bot.send_message(
                chat_id=ADMIN_ID,
                text=admin_text,
                reply_markup=get_admin_request_keyboard(callback_data.req_id),
            )


@router.callback_query(UserPaymentCallback.filter(F.action == "cancel"))
async def user_cancel(callback: CallbackQuery, callback_data: UserPaymentCallback, bot: Bot) -> None:
    """User cancels payment - cancel request."""
    decline_pending_request(callback_data.req_id)

    user_text = """
<b>❌ Заявка отменена</b>

Вы можете оформить подписку позже.
"""
    try:
        await callback.message.edit_text(user_text, parse_mode="HTML", reply_markup=get_back_to_menu_keyboard())
    except Exception:
        await callback.message.edit_caption(caption=user_text, parse_mode="HTML", reply_markup=get_back_to_menu_keyboard())

    await callback.answer("Заявка отменена")

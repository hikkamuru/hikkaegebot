"""Admin handlers — confirm/decline payment requests."""
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from config import ADMIN_ID
from keyboards import AdminRequestCallback, get_admin_request_keyboard
from data import get_pending_request, confirm_pending_request, decline_pending_request
from datetime import datetime, timedelta

router = Router()


def is_admin(user_id: int) -> bool:
    """Check if user is admin."""
    return ADMIN_ID and user_id == ADMIN_ID


@router.callback_query(AdminRequestCallback.filter(F.action == "ok"))
async def admin_confirm_payment(
    callback: CallbackQuery, callback_data: AdminRequestCallback, bot: Bot
) -> None:
    """Admin confirms payment — user gets the subscription."""
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return

    req = get_pending_request(callback_data.req_id)
    if not req:
        await callback.answer("Заявка уже обработана", show_alert=True)
        return

    purchased = confirm_pending_request(callback_data.req_id)
    if not purchased:
        await callback.answer("Ошибка", show_alert=True)
        return

    # Calculate expiration date
    expiration_date = (datetime.now() + timedelta(days=30)).strftime("%d.%m.%Y")

    user_text = f"""
<b>✅ Подписка подключена!</b>

🎉 Поздравляем! Ваша подписка <b>{purchased.name.replace('️', '')}</b> активирована

📅 Действует до: <b>{expiration_date}</b>
📆 30 дней с момента подключения

<b>🎫 Ваш код:</b> <code>{purchased.code}</code>

━━━━━━━━━━━━━━━━━━━━━━
<b>📋 Правила использования:</b>
• ☕️ 1 напиток в день
• 🕐 Действует 30 дней
• 📱 Называйте свое ФИО при получении кофе

<b>🎁 Бонус:</b> 10% скидка на выпечку

<i>Приятного кофе в «Бариста»! ☕️</i>
"""
    try:
        await bot.send_message(chat_id=req.user_id, text=user_text, parse_mode="HTML")
    except Exception:
        pass  # User may have blocked the bot

    # Update admin message
    admin_text = f"""
<b>✅ Оплата подтверждена</b>

━━━━━━━━━━━━━━━━━━━━━━
<b>👤 Клиент:</b> {req.full_name}
<b>📞 Телефон:</b> {req.phone}
<b>🔗 Username:</b> @{req.username or 'нет'}
━━━━━━━━━━━━━━━━━━━━━━

<b>📦 Подписка:</b> {req.card_name}
<b>💰 Сумма:</b> {req.price:,} ₽

<b>🎫 Код:</b> <code>{purchased.code}</code>
<b>📅 Истекает:</b> {expiration_date}

✅ Подписка активирована
"""
    try:
        await callback.message.edit_caption(caption=admin_text, parse_mode="HTML", reply_markup=None)
    except Exception:
        await callback.message.edit_text(admin_text, reply_markup=None)

    await callback.answer("Оплата подтверждена!")


@router.callback_query(AdminRequestCallback.filter(F.action == "no"))
async def admin_decline_payment(
    callback: CallbackQuery, callback_data: AdminRequestCallback, bot: Bot
) -> None:
    """Admin declines payment."""
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return

    req = get_pending_request(callback_data.req_id)
    if not req:
        await callback.answer("Заявка уже обработана", show_alert=True)
        return

    decline_pending_request(callback_data.req_id)

    # Notify user
    user_text = """
<b>❌ Заявка отклонена</b>

К сожалению, ваша заявка на подписку не была подтверждена.

📞 Если вы уже оплатили — свяжитесь с администратором кофейни «Бариста»
"""
    try:
        await bot.send_message(chat_id=req.user_id, text=user_text, parse_mode="HTML")
    except Exception:
        pass

    # Update admin message
    admin_text = f"""
<b>❌ Заявка отклонена</b>

━━━━━━━━━━━━━━━━━━━━━━
<b>👤 Клиент:</b> {req.full_name}
<b>📞 Телефон:</b> {req.phone}
<b>🔗 Username:</b> @{req.username or 'нет'}
━━━━━━━━━━━━━━━━━━━━━━

<b>📦 Подписка:</b> {req.card_name}
<b>💰 Сумма:</b> {req.price:,} ₽

❌ Заявка отклонена
"""
    try:
        await callback.message.edit_caption(caption=admin_text, parse_mode="HTML", reply_markup=None)
    except Exception:
        await callback.message.edit_text(admin_text, reply_markup=None)

    await callback.answer("Заявка отклонена")

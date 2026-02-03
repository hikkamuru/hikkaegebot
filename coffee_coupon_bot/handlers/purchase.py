"""Purchase handlers with conversation for collecting user info."""
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, InputMediaPhoto, Message
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from keyboards import (
    get_back_to_menu_keyboard,
    get_payment_keyboard,
    CardCallback,
)
from data import IMAGES, get_card_by_id, add_pending_request

router = Router()


# FSM states for purchase process
class PurchaseState(StatesGroup):
    """States for purchase process."""
    name_input = State()
    phone_input = State()


# Payment details - UPDATE THIS WITH ACTUAL PAYMENT INFO
PAYMENT_DETAILS = """
<b>💳 Реквизиты для оплаты:</b>

<b>Карта:</b> 4276 0800 1343 3843
<b>Получатель:</b> Павел Александрович М.
<b>Сумма:</b> {} ₽
"""


@router.callback_query(CardCallback.filter(F.action == "buy"))
async def start_purchase(
    callback: CallbackQuery, callback_data: CardCallback, bot: Bot, state: FSMContext
) -> None:
    """Start purchase process - ask for full name."""
    card = get_card_by_id(callback_data.card_id)
    if not card:
        await callback.answer("Подписка не найдена", show_alert=True)
        return

    # Store selected card
    await state.update_data(card_id=card.id, card_name=card.name, price=card.price)

    caption = """
<b>📝 Оформление подписки</b>

Пожалуйста, введите <b>Ваше ФИО</b> (как в паспорте):

<i>Например: Иванов Иван Иванович</i>
"""

    try:
        await callback.message.edit_media(
            media=InputMediaPhoto(media=IMAGES["coffee_all"], caption=caption, parse_mode="HTML"),
        )
    except Exception:
        await callback.message.edit_text(caption, parse_mode="HTML")

    await state.set_state(PurchaseState.name_input)
    await callback.answer()


@router.message(StateFilter(PurchaseState.name_input))
async def process_name(message: Message, state: FSMContext) -> None:
    """Process full name input and ask for phone."""
    full_name = message.text.strip()
    if len(full_name) < 3:
        await message.answer("Пожалуйста, введите полное ФИО (минимум 3 символа):")
        return

    await state.update_data(full_name=full_name)

    caption = """
<b>📝 Оформление подписки</b>

<b>ФИО:</b> {}

Теперь введите <b>номер телефона</b>:

<i>Например: +7 999 123 45 67 или 8 999 123 45 67</i>
""".format(full_name)

    await message.answer(caption, parse_mode="HTML")
    await state.set_state(PurchaseState.phone_input)


@router.message(StateFilter(PurchaseState.phone_input))
async def process_phone(message: Message, bot: Bot, state: FSMContext) -> None:
    """Process phone input and send payment details."""
    phone = message.text.strip()

    # Simple phone validation
    phone_digits = "".join(c for c in phone if c.isdigit())
    if len(phone_digits) < 10:
        await message.answer("Пожалуйста, введите корректный номер телефона:")
        return

    await state.update_data(phone=phone)

    # Get stored data
    data = await state.get_data()
    card_id = data.get("card_id")
    card_name = data.get("card_name")
    full_name = data.get("full_name")
    price = data.get("price")

    card = get_card_by_id(card_id)
    if not card:
        await message.answer("Подписка не найдена", reply_markup=get_back_to_menu_keyboard())
        await state.clear()
        return

    user = message.from_user

    # Create pending request (NOT sent to admin yet)
    pending = add_pending_request(
        user_id=user.id,
        username=user.username or "",
        full_name=full_name,
        phone=phone,
        card=card,
    )

    # Clear state
    await state.clear()

    # Send payment details to user with buttons
    payment_text = PAYMENT_DETAILS.format(price)

    user_caption = f"""
<b>✅ Заявка создана!</b>

<b>Подписка:</b> {card_name.replace('️', '')}
<b>Сумма:</b> {price:,} ₽

{payment_text}

<i>После оплаты нажмите кнопку «Оплатил»</i>
"""

    await message.answer(
        user_caption, 
        reply_markup=get_payment_keyboard(pending.id), 
        parse_mode="HTML"
    )

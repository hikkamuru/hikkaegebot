"""Catalog and menu handlers."""
from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup

from keyboards import (
    get_main_menu_keyboard,
    get_catalog_keyboard,
    get_back_to_menu_keyboard,
    MenuCallback,
)
from data import IMAGES, SUBSCRIPTION_CARDS

router = Router()

MAIN_MENU_TEXT = """<b>☕️ КОФЕ ПО ПОДПИСКЕ</b>

<i>Заведи подписку и пей любимый кофе каждый день по фиксированной цене.</i>

<b>Тарифы:</b>
☕️ <b>БАЗОВЫЙ</b> — эспрессо, американо — 1 680₽/мес
🥛 <b>МОЛОЧНЫЙ</b> — + капучино, латте — 2 850₽/мес
🌟 <b>ВСЕ ВКЛЮЧЕНО</b> — весь ассортимент — 3 580₽/мес

<b>📋 1 напиток в день, 30 дней</b>

<i>Выберите подписку и оформите заявку!</i> ☕️"""

INFO_TEXT = """<b>💡 Как оформить подписку</b>

<b>1️⃣</b> Выберите подписку в каталоге

<b>2️⃣</b> Введите ФИО и номер телефона

<b>3️⃣</b> Оплатите по реквизитам

<b>4️⃣</b> Администратор подтвердит оплату

<b>5️⃣</b> Получите код для кофе

<b>☕️</b> 1 напиток в день, 30 дней с активации"""

CATALOG_TEXT = """<b>📋 Выберите подписку</b>

<i>Тарифы и цены:</i>"""


@router.callback_query(MenuCallback.filter(F.action == "main"))
async def show_main_menu(callback: CallbackQuery, callback_data: MenuCallback) -> None:
    """Show main menu."""
    try:
        await callback.message.edit_media(
            media=InputMediaPhoto(media=IMAGES["welcome"], caption=MAIN_MENU_TEXT, parse_mode="HTML"),
            reply_markup=get_main_menu_keyboard(),
        )
    except Exception:
        await callback.message.edit_text(
            MAIN_MENU_TEXT,
            reply_markup=get_main_menu_keyboard(),
        )
    await callback.answer()


@router.callback_query(MenuCallback.filter(F.action == "catalog"))
async def show_catalog(callback: CallbackQuery, callback_data: MenuCallback) -> None:
    """Show subscription cards catalog."""
    lines = [CATALOG_TEXT]
    for c in SUBSCRIPTION_CARDS:
        lines.append(f"\n<b>{c.name}</b> — {c.price:,} ₽/мес")
        lines.append(f"<i>{c.details}</i>")
    caption = "\n".join(lines)

    try:
        await callback.message.edit_media(
            media=InputMediaPhoto(media=IMAGES["coffee_all"], caption=caption, parse_mode="HTML"),
            reply_markup=get_catalog_keyboard(),
        )
    except Exception:
        await callback.message.edit_text(
            caption,
            reply_markup=get_catalog_keyboard(),
        )
    await callback.answer()


@router.callback_query(MenuCallback.filter(F.action == "info"))
async def show_info(callback: CallbackQuery, callback_data: MenuCallback) -> None:
    """Show how it works."""
    try:
        await callback.message.edit_media(
            media=InputMediaPhoto(media=IMAGES["welcome"], caption=INFO_TEXT, parse_mode="HTML"),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="◀️ Назад", callback_data=MenuCallback(action="main").pack())
            ]]),
        )
    except Exception:
        await callback.message.edit_text(
            INFO_TEXT,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="◀️ Назад", callback_data=MenuCallback(action="main").pack())
            ]]),
        )
    await callback.answer()

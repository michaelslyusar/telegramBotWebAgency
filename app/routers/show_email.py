"""
WWWizards Telegram Bot - Menu Router
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery
from loguru import logger

from app.constants import CallbackData,COMPANY_INFO
from app.keyboards.main_menu import get_main_menu_keyboard
from app.logging_config import log_user_action

router = Router()


@router.callback_query(F.data == CallbackData.SHOW_EMAIL.value)
async def show_main_menu(callback: CallbackQuery) -> None:
    """Show main menu."""
    user = callback.from_user
    log_user_action(user_id=user.id, action="show_main_menu")

    text = f'📧 Email us: <a href="mailto:{COMPANY_INFO["email"]}">{COMPANY_INFO["email"]}</a>'

    await callback.message.edit_text(
        text=text,
        parse_mode="HTML",
        reply_markup=get_main_menu_keyboard()
    )
    await callback.answer()


"""
WWWizards Telegram Bot - Menu Router
"""
from aiogram import Router,F
from aiogram.types import CallbackQuery
from loguru import logger

from app.constants import CallbackData
from app.keyboards.main_menu import get_main_menu_keyboard
from app.logging_config import log_user_action

router = Router()


@router.callback_query(F.data == CallbackData.MAIN_MENU.value)
@router.callback_query(F.data == CallbackData.BACK_TO_MENU.value)
async def show_main_menu(callback: CallbackQuery) -> None:
    """Show main menu."""
    user = callback.from_user
    log_user_action(user_id=user.id, action="show_main_menu")
    
    menu_text = (
        "🏠 <b>Главное меню</b>\n\n"
        "Выберите нужную опцию:"
    )
    
    await callback.message.edit_text(
        text=menu_text,
        reply_markup=get_main_menu_keyboard(user.id)
    )
    await callback.answer()





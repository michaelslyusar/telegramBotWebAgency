"""
WWWizards Telegram Bot - Contact Router
"""
from aiogram import Router,F
from aiogram.types import CallbackQuery
from loguru import logger

from app.constants import CallbackData, COMPANY_INFO
from app.keyboards.contact import get_contact_keyboard
from app.logging_config import log_user_action
from app.services.notifications import NotificationService

router = Router()


@router.callback_query(F.text(CallbackData.CONTACT_MANAGER))
async def show_contact_manager(callback: CallbackQuery) -> None:
    """Show contact manager information."""
    user = callback.from_user
    log_user_action(user_id=user.id, action="show_contact_manager")
    
    # Send notification to manager about contact request
    try:
        notification_service = NotificationService()
        await notification_service.notify_contact_request(user)
    except Exception as e:
        logger.error(f"Error sending contact notification: {e}")
    
    contact_text = (
        "👨‍💼 <b>Связаться с менеджером</b>\n\n"
        "Наш менеджер готов ответить на ваши вопросы и помочь с выбором подходящих услуг.\n\n"
        "<b>Способы связи:</b>\n"
        f"📧 Email: {COMPANY_INFO['email']}\n"
        f"📱 Telegram: {COMPANY_INFO['telegram']}\n"
        f"🌐 Сайт: {COMPANY_INFO['website_ru']}\n\n"
        "Выберите удобный способ связи:"
    )
    
    await callback.message.edit_text(
        text=contact_text,
        reply_markup=get_contact_keyboard()
    )
    await callback.answer()


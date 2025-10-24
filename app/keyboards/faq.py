"""
WWWizards Telegram Bot - FAQ Keyboard
"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.constants import CallbackData


def get_faq_keyboard() -> InlineKeyboardMarkup:
    """Create FAQ keyboard."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📄 Скачать PDF каталог",
                    callback_data="download_pdf"
                )
            ],
            [
                InlineKeyboardButton(
                    text="👨‍💼 Связаться с менеджером",
                    callback_data=CallbackData.CONTACT_MANAGER
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠 Главное меню",
                    callback_data=CallbackData.BACK_TO_MENU
                )
            ]
        ]
    )
    return keyboard


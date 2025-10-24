"""
WWWizards Telegram Bot - Contact Keyboard
"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.constants import CallbackData, COMPANY_INFO


def get_contact_keyboard() -> InlineKeyboardMarkup:
    """Create contact manager keyboard."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📧 Написать на email",
                    url=f"mailto:{COMPANY_INFO['email']}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📱 Написать в Telegram",
                    url=f"https://t.me/{COMPANY_INFO['telegram'].lstrip('@')}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🌐 Наш сайт",
                    url=COMPANY_INFO["website_ru"]
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


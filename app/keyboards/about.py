"""
WWWizards Telegram Bot - About Us Keyboard
"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.constants import CallbackData, COMPANY_INFO


def get_about_keyboard() -> InlineKeyboardMarkup:
    """Create about us keyboard with company links."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🌐 Наш сайт (RU)",
                    url=COMPANY_INFO["website_ru"]
                ),
                InlineKeyboardButton(
                    text="🌍 Our Website (EN)",
                    url=COMPANY_INFO["website_com"]
                )
            ],
            [
                InlineKeyboardButton(
                    text="📧 Email",
                    callback_data=CallbackData.SHOW_EMAIL.value
                ),
                InlineKeyboardButton(
                    text="📱 Telegram",
                    url=f"https://t.me/{COMPANY_INFO['telegram'].lstrip('@')}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💬 Начать чат",
                    callback_data=CallbackData.START_CHAT.value
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Вернуться",
                    callback_data=CallbackData.BACK_TO_MENU.value
                )
            ]
        ]
    )
    return keyboard


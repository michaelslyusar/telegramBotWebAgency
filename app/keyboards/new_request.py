"""
WWWizards Telegram Bot - Services Keyboard
"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.constants import CallbackData

"""     Main Services Keyboard      """
def get_new_request_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Вернуться",
                    callback_data=CallbackData.BACK_TO_MENU
                )
            ]
        ]
    )
    return keyboard
"""
WWWizards Telegram Bot - Main Menu Keyboard
"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from loguru import logger
from app.constants import CallbackData

""" Main Menu under the chat window """


def get_main_menu_keyboard(user_id) -> ReplyKeyboardMarkup:
    url = f"https://hillagagusil.beget.app/quick-launch?uid={user_id}"

    """Create main menu keyboard."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=CallbackData.MAIN_MENU_ABOUT.value
                ),
            ],
            [
                KeyboardButton(
                    text=CallbackData.MAIN_MENU_SERVICES.value
                )
            ],
            [
                KeyboardButton(
                    text=CallbackData.MAIN_MENU_ORDER_WEBSITE.value,
                    web_app=WebAppInfo(url=url)
                ),
                KeyboardButton(
                    text=CallbackData.MAIN_MENU_MANAGER.value
                )
            ],
            [
                KeyboardButton(
                    text=CallbackData.MAIN_MENU_CHAT.value
                ),
                KeyboardButton(
                    text=CallbackData.MAIN_MENU_FAQ.value
                )
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_back_to_menu_keyboard() -> InlineKeyboardMarkup:
    """Create back to menu keyboard."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🏠 Главное меню",
                    callback_data=CallbackData.BACK_TO_MENU.value
                )
            ]
        ]
    )
    return keyboard

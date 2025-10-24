"""
WWWizards Telegram Bot - About Router
"""
from aiogram import Router,F
from aiogram.types import CallbackQuery,Message
from loguru import logger

from app.constants import CallbackData, COMPANY_INFO
from app.keyboards.about import get_about_keyboard
from app.logging_config import log_user_action

router = Router()


@router.message(F.text == CallbackData.MAIN_MENU_ABOUT.value)
async def show_about_us(message: Message) -> None:
    user = message.from_user
    log_user_action(user_id=user.id, action="show_about_us")

    about_text = (
        f"🏢 <b>О компании {COMPANY_INFO['name']}</b>\n\n"
        f"{COMPANY_INFO['description']}\n\n"
        "<b>Наши преимущества:</b>\n"
        "• 5+ лет опыта в веб-разработке\n"
        "• Современные технологии и подходы\n"
        "• Индивидуальный подход к каждому проекту\n"
        "• Полный цикл разработки\n"
        "• Техническая поддержка после запуска\n"
        "• Прозрачное ценообразование\n\n"
        "<b>Свяжитесь с нами:</b>"
    )
    await message.answer(
        text=about_text,
        reply_markup=get_about_keyboard()
    )


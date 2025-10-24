"""
WWWizards Telegram Bot - Start Router
"""
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.methods import SetChatMenuButton
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, MenuButtonWebApp, WebAppInfo

from app.keyboards.main_menu import get_main_menu_keyboard
from app.logging_config import log_user_action

router = Router()

@router.message(CommandStart())
async def start_command(message: Message) -> None:
    """Handle /start command."""
    user = message.from_user
    log_user_action(
        user_id=user.id,
        action="start_command",
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    
    welcome_text = (
        f"👋 Привет, {user.first_name}!\n\n"
        "Добро пожаловать в <b>WWWizards</b> - профессиональную веб-студию!\n\n"
        "Мы создаем современные и эффективные веб-решения для вашего бизнеса:\n"
        "• Корпоративные сайты\n"
        "• Лендинги\n"
        "• Интернет-магазины\n"
        "• Каталоги товаров\n"
        "• Редизайн сайтов\n"
        "• Техническая поддержка\n\n"
        "Выберите нужную опцию в меню ниже:"
    )

    await message.bot(SetChatMenuButton(
        menu_button=MenuButtonWebApp(text="Open Web App", web_app=WebAppInfo(url="https://michaelslyusar.github.io/"))
    ))
    await message.answer(
        text=welcome_text,
        reply_markup=get_main_menu_keyboard(user.id)
    )


@router.message(Command("help"))
async def help_command(message: Message) -> None:
    """Handle /help command."""
    user = message.from_user
    log_user_action(user_id=user.id, action="help_command")
    
    help_text = (
        "🤖 <b>WWWizards Bot - Справка</b>\n\n"
        "<b>Доступные команды:</b>\n"
        "/start - Запустить бота и показать главное меню\n"
        "/menu - Вернуться в главное меню\n"
        "/help - Показать эту справку\n\n"
        "<b>Основные функции:</b>\n"
        "• Просмотр информации о компании\n"
        "• Каталог услуг с ценами\n"
        "• Заказ сайта через интерактивную форму\n"
        "• Связь с менеджером\n"
        "• FAQ и документация\n\n"
        "Используйте кнопки меню для навигации по боту."
    )
    
    await message.answer(
        text=help_text,
        reply_markup=get_main_menu_keyboard()
    )


@router.message(Command("menu"))
async def menu_command(message: Message) -> None:
    """Handle /menu command."""
    user = message.from_user
    log_user_action(user_id=user.id, action="menu_command")
    
    menu_text = (
        "🏠 <b>Главное меню</b>\n\n"
        "Выберите нужную опцию:"
    )
    
    await message.answer(
        text=menu_text,
        reply_markup=get_main_menu_keyboard()
    )


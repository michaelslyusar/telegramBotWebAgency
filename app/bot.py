"""
WWWizards Telegram Bot - Bot Instance and Setup
"""
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from loguru import logger

from app.config import settings
from app.middlewares.logging import LoggingMiddleware
from app.middlewares.throttling import ThrottlingMiddleware
from app.routers import (
    about,
    contact,
    faq,
    menu,
    order_quiz,
    services,
    start,
    show_email,
    new_request, new_order
)


def create_bot() -> Bot:
    """Create and configure the bot instance."""
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview_is_disabled=True,
        ),
    )
    
    logger.info("Bot instance created successfully")
    return bot


def create_dispatcher() -> Dispatcher:
    """Create and configure the dispatcher with all routers and middlewares."""
    dp = Dispatcher()
    
    # Add middlewares
    # dp.message.middleware(LoggingMiddleware())
    # dp.callback_query.middleware(LoggingMiddleware())
    # dp.message.middleware(ThrottlingMiddleware())
    # dp.callback_query.middleware(ThrottlingMiddleware())
    
    # Include routers
    dp.include_router(start.router)
    # dp.include_router(menu.router)
    dp.include_router(about.router)
    dp.include_router(services.router)
    dp.include_router(order_quiz.router)
    dp.include_router(contact.router)
    dp.include_router(faq.router)
    dp.include_router(show_email.router)
    dp.include_router(new_request.router)
    dp.include_router(new_order.router)

    logger.info("Dispatcher configured with all routers and middlewares")
    return dp


async def setup_bot() -> tuple[Bot, Dispatcher]:
    """Setup bot and dispatcher for use."""
    bot = create_bot()
    dp = create_dispatcher()
    
    # Set dispatcher for the bot
    await dp.start_polling(bot)
    bot_info = await bot.get_me()
    # Get bot info
    try:
        bot_info = await bot.get_me()
        logger.info(f"Bot @{bot_info.username} is ready")
    except Exception as e:
        logger.error(f"Failed to get bot info: {e}")
        raise
    
    return bot, dp


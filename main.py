"""
WWWizards Telegram Bot - Main Entry Point
"""
import asyncio
import sys
from pathlib import Path

from loguru import logger

from app.bot import create_bot,create_dispatcher
from app.config import settings
from app.logging_config import setup_logging
from app.db.db import async_main


async def main() -> None:
    """Main application entry point."""
    # Setup logging
    setup_logging()

    logger.info("Starting WWWizards Telegram Bot...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")

    try:
        await async_main()
        logger.info("Database was connected successfully.")
    except Exception as e:
        logger.error(f"Failed to connect to DB : {e}")
    bot = create_bot()
    dp = create_dispatcher()

    try:
        bot_info = await bot.get_me()
        logger.info(f"Bot @{bot_info.username} is ready")
    except Exception as e:
        logger.error(f"Failed to get bot info: {e}")
        raise

    try:
        logger.info("Bot is starting...")
        await dp.start_polling(bot)
        # Get bot info
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        sys.exit(1)
    finally:
        logger.info("Bot shutdown complete")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Application failed to start: {e}")
        sys.exit(1)


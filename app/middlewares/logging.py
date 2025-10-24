"""
WWWizards Telegram Bot - Logging Middleware
"""
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject
from loguru import logger

from app.logging_config import log_user_action


class LoggingMiddleware(BaseMiddleware):
    """Middleware for logging user interactions."""
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """Process event with logging."""
        user = None
        event_type = type(event).__name__
        
        # Extract user information
        if isinstance(event, Message):
            user = event.from_user
            log_user_action(
                user_id=user.id,
                action="message",
                message_type=event.content_type,
                text=event.text[:100] if event.text else None,
                username=user.username,
                first_name=user.first_name
            )
        elif isinstance(event, CallbackQuery):
            user = event.from_user
            log_user_action(
                user_id=user.id,
                action="callback_query",
                callback_data=event.data,
                username=user.username,
                first_name=user.first_name
            )
        
        # Log the event
        if user:
            logger.info(
                f"Processing {event_type} from user {user.id} (@{user.username})"
            )
        else:
            logger.info(f"Processing {event_type}")
        
        # Call the handler
        try:
            result = await handler(event, data)
            logger.debug(f"Handler completed successfully for {event_type}")
            return result
        except Exception as e:
            logger.error(f"Handler failed for {event_type}: {e}")
            raise


"""
WWWizards Telegram Bot - Throttling Middleware
"""
import asyncio
from typing import Callable, Dict, Any, Awaitable
from collections import defaultdict
from datetime import datetime, timedelta

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject
from loguru import logger

from app.config import settings


class ThrottlingMiddleware(BaseMiddleware):
    """Middleware for rate limiting user requests."""
    
    def __init__(self):
        """Initialize throttling middleware."""
        self.rate = settings.THROTTLE_RATE
        self.burst = settings.THROTTLE_BURST
        self.user_requests = defaultdict(list)
        self.cleanup_interval = 300  # 5 minutes
        self.last_cleanup = datetime.now()
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """Process event with throttling."""
        user_id = None
        
        # Extract user ID
        if isinstance(event, (Message, CallbackQuery)):
            user_id = event.from_user.id
        
        if not user_id:
            # No user ID, skip throttling
            return await handler(event, data)
        
        # Cleanup old requests periodically
        await self._cleanup_old_requests()
        
        # Check if user is rate limited
        if await self._is_rate_limited(user_id):
            logger.warning(f"User {user_id} is rate limited")
            
            if isinstance(event, Message):
                await event.answer(
                    "⏳ Слишком много запросов. Пожалуйста, подождите немного.",
                    show_alert=True
                )
            elif isinstance(event, CallbackQuery):
                await event.answer(
                    "⏳ Слишком много запросов. Пожалуйста, подождите немного.",
                    show_alert=True
                )
            
            return
        
        # Record this request
        await self._record_request(user_id)
        
        # Call the handler
        return await handler(event, data)
    
    async def _is_rate_limited(self, user_id: int) -> bool:
        """Check if user is rate limited."""
        now = datetime.now()
        user_requests = self.user_requests[user_id]
        
        # Remove old requests outside the rate window
        cutoff_time = now - timedelta(seconds=self.rate)
        user_requests[:] = [req_time for req_time in user_requests if req_time > cutoff_time]
        
        # Check if user has exceeded burst limit
        return len(user_requests) >= self.burst
    
    async def _record_request(self, user_id: int) -> None:
        """Record a request for the user."""
        now = datetime.now()
        self.user_requests[user_id].append(now)
    
    async def _cleanup_old_requests(self) -> None:
        """Clean up old request records."""
        now = datetime.now()
        
        # Only cleanup every 5 minutes
        if (now - self.last_cleanup).seconds < self.cleanup_interval:
            return
        
        self.last_cleanup = now
        cutoff_time = now - timedelta(hours=1)  # Keep 1 hour of history
        
        # Remove old user request records
        users_to_remove = []
        for user_id, requests in self.user_requests.items():
            # Remove old requests
            requests[:] = [req_time for req_time in requests if req_time > cutoff_time]
            
            # Remove users with no recent requests
            if not requests:
                users_to_remove.append(user_id)
        
        for user_id in users_to_remove:
            del self.user_requests[user_id]
        
        logger.debug(f"Cleaned up throttling data for {len(users_to_remove)} users")


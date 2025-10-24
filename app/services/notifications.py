"""
WWWizards Telegram Bot - Notification Service
"""
import asyncio
from typing import Optional

from aiogram import Bot
from loguru import logger

from app.config import settings
from app.schemas.lead import LeadData


class NotificationService:
    """Service for sending notifications to managers."""
    
    def __init__(self):
        """Initialize notification service."""
        self.bot = Bot(token=settings.BOT_TOKEN)
        self.manager_chat_id = settings.MANAGER_CHAT_ID
        self.enabled = settings.NOTIFICATION_ENABLED
        self.retry_attempts = settings.NOTIFICATION_RETRY_ATTEMPTS
        self.retry_delay = settings.NOTIFICATION_RETRY_DELAY
    
    async def notify_new_lead(self, lead_data: LeadData) -> bool:
        """Send notification about new lead."""
        if not self.enabled:
            logger.info("Notifications disabled, skipping new lead notification")
            return True
        
        message = self._format_new_lead_message(lead_data)
        return await self._send_notification(message, "new_lead")
    
    async def notify_contact_request(self, user) -> bool:
        """Send notification about contact request."""
        if not self.enabled:
            logger.info("Notifications disabled, skipping contact request notification")
            return True
        
        message = self._format_contact_request_message(user)
        return await self._send_notification(message, "contact_request")
    
    async def notify_system_alert(self, alert_message: str) -> bool:
        """Send system alert notification."""
        if not self.enabled:
            logger.info("Notifications disabled, skipping system alert")
            return True
        
        message = f"🚨 <b>System Alert</b>\n\n{alert_message}"
        return await self._send_notification(message, "system_alert")
    
    def _format_new_lead_message(self, lead_data: LeadData) -> str:
        """Format new lead notification message."""
        user_info = f"👤 {lead_data.first_name or 'Unknown'}"
        if lead_data.last_name:
            user_info += f" {lead_data.last_name}"
        if lead_data.username:
            user_info += f" (@{lead_data.username})"
        
        message = (
            f"🎯 <b>Новая заявка!</b>\n\n"
            f"{user_info}\n"
            f"🆔 ID: {lead_data.user_id}\n"
            f"🏢 Компания: {lead_data.company_name}\n"
            f"📞 Телефон: {lead_data.contact_phone}\n"
            f"📧 Email: {lead_data.contact_email}\n\n"
            f"<b>Проект:</b>\n"
            f"• Тип услуги: {lead_data.service_type}\n"
            f"• Бюджет: {lead_data.budget}\n"
            f"• Сроки: {lead_data.timeline}\n\n"
        )
        
        if lead_data.additional_info:
            message += f"<b>Дополнительная информация:</b>\n{lead_data.additional_info}\n\n"
        
        message += f"💬 <a href='tg://user?id={lead_data.user_id}'>Написать пользователю</a>"
        
        return message
    
    def _format_contact_request_message(self, user) -> str:
        """Format contact request notification message."""
        user_info = f"👤 {user.first_name or 'Unknown'}"
        if user.last_name:
            user_info += f" {user.last_name}"
        if user.username:
            user_info += f" (@{user.username})"
        
        message = (
            f"📞 <b>Запрос на связь с менеджером</b>\n\n"
            f"{user_info}\n"
            f"🆔 ID: {user.id}\n\n"
            f"💬 <a href='tg://user?id={user.id}'>Написать пользователю</a>"
        )
        
        return message
    
    async def _send_notification(self, message: str, notification_type: str) -> bool:
        """Send notification with retry logic."""
        for attempt in range(self.retry_attempts):
            try:
                await self.bot.send_message(
                    chat_id=self.manager_chat_id,
                    text=message,
                    parse_mode="HTML",
                    disable_web_page_preview=True
                )
                
                logger.info(f"Notification sent successfully: {notification_type}")
                return True
                
            except Exception as e:
                logger.warning(
                    f"Failed to send notification (attempt {attempt + 1}/{self.retry_attempts}): {e}"
                )
                
                if attempt < self.retry_attempts - 1:
                    await asyncio.sleep(self.retry_delay)
                else:
                    logger.error(f"Failed to send notification after {self.retry_attempts} attempts: {e}")
                    return False
        
        return False
    
    async def close(self) -> None:
        """Close the bot instance."""
        await self.bot.session.close()


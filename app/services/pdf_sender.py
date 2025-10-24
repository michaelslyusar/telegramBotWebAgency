"""
WWWizards Telegram Bot - PDF Sender Service
"""
from pathlib import Path
from typing import Optional

from aiogram import Bot
from aiogram.types import FSInputFile
from loguru import logger

from app.config import settings


class PDFSenderService:
    """Service for sending PDF files."""
    
    def __init__(self):
        """Initialize PDF sender service."""
        self.bot = Bot(token=settings.BOT_TOKEN)
        self.pdf_path = settings.pdf_faq_path
    
    async def send_faq_pdf(self, chat_id: int, filename: str = "WWWizards_FAQ.pdf") -> bool:
        """Send FAQ PDF file to user."""
        try:
            if not self.pdf_path.exists():
                logger.error(f"FAQ PDF file not found: {self.pdf_path}")
                return False
            
            pdf_file = FSInputFile(self.pdf_path, filename=filename)
            
            await self.bot.send_document(
                chat_id=chat_id,
                document=pdf_file,
                caption=(
                    "📄 <b>WWWizards - FAQ и каталог услуг</b>\n\n"
                    "В этом документе вы найдете подробную информацию о наших услугах, "
                    "процессе работы и часто задаваемых вопросах."
                ),
                parse_mode="HTML"
            )
            
            logger.info(f"FAQ PDF sent successfully to chat {chat_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending FAQ PDF: {e}")
            return False
    
    async def send_custom_pdf(self, chat_id: int, pdf_path: Path, filename: str, caption: str = "") -> bool:
        """Send custom PDF file to user."""
        try:
            if not pdf_path.exists():
                logger.error(f"PDF file not found: {pdf_path}")
                return False
            
            pdf_file = FSInputFile(pdf_path, filename=filename)
            
            await self.bot.send_document(
                chat_id=chat_id,
                document=pdf_file,
                caption=caption,
                parse_mode="HTML"
            )
            
            logger.info(f"Custom PDF sent successfully to chat {chat_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending custom PDF: {e}")
            return False
    
    async def close(self) -> None:
        """Close the bot instance."""
        await self.bot.session.close()


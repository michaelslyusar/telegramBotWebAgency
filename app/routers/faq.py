"""
WWWizards Telegram Bot - FAQ Router
"""
from aiogram import Router,F
from aiogram.types import CallbackQuery, FSInputFile
from loguru import logger

from app.constants import CallbackData
from app.config import settings
from app.keyboards.faq import get_faq_keyboard
from app.logging_config import log_user_action

router = Router()


@router.callback_query(F.text(CallbackData.FAQ_CONTENT))
async def show_faq(callback: CallbackQuery) -> None:
    """Show FAQ content."""
    user = callback.from_user
    log_user_action(user_id=user.id, action="show_faq")
    
    await callback.message.edit_text(
        text=CallbackData.FAQ_CONTENT,
        reply_markup=get_faq_keyboard()
    )
    await callback.answer()


@router.callback_query(F.text("download_pdf"))
async def download_pdf(callback: CallbackQuery) -> None:
    """Send FAQ PDF file."""
    user = callback.from_user
    log_user_action(user_id=user.id, action="download_pdf")
    
    try:
        # Check if PDF file exists
        pdf_path = settings.pdf_faq_path
        if not pdf_path.exists():
            await callback.answer(
                "PDF файл временно недоступен. Попробуйте позже.",
                show_alert=True
            )
            return
        
        # Send PDF file
        pdf_file = FSInputFile(pdf_path, filename="WWWizards_FAQ.pdf")
        await callback.message.answer_document(
            document=pdf_file,
            caption="📄 <b>WWWizards - FAQ и каталог услуг</b>\n\n"
                   "В этом документе вы найдете подробную информацию о наших услугах, "
                   "процессе работы и часто задаваемых вопросах."
        )
        
        await callback.answer("PDF файл отправлен!")
        
    except Exception as e:
        logger.error(f"Error sending PDF: {e}")
        await callback.answer(
            "Ошибка при отправке PDF файла. Попробуйте позже.",
            show_alert=True
        )


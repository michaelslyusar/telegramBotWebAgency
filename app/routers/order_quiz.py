"""
WWWizards Telegram Bot - Order Quiz Router
"""
from aiogram import Router,F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

from app.constants import CallbackData
from app.keyboards.main_menu import get_back_to_menu_keyboard
from app.logging_config import log_user_action
from app.schemas.lead import LeadData
from app.services.notifications import NotificationService
from app.services.storage_base import StorageService
from app.states.order import OrderStates

router = Router()


@router.callback_query(F.text(CallbackData.ORDER_WEBSITE))
async def start_order_quiz(callback: CallbackQuery, state: FSMContext) -> None:
    """Start the order quiz."""
    user = callback.from_user
    log_user_action(user_id=user.id, action="start_order_quiz")
    
    # Initialize quiz data
    await state.update_data(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        current_question=0,
        answers={}
    )
    
    # Show first question
    await show_question(callback, state)
    await callback.answer()


async def show_question(callback: CallbackQuery, state: FSMContext) -> None:
    """Show current question."""
    data = await state.get_data()
    current_question = data.get("current_question", 0)
    
    if current_question >= len(CallbackData.ORDER_QUIZ_QUESTIONS):
        await finish_quiz(callback, state)
        return
    
    question = CallbackData.ORDER_QUIZ_QUESTIONS[current_question]
    
    question_text = f"<b>Вопрос {current_question + 1} из {len(CallbackData.ORDER_QUIZ_QUESTIONS)}</b>\n\n{question['question']}"
    
    if question["type"] == "choice":
        keyboard_buttons = []
        for option in question["options"]:
            keyboard_buttons.append([
                InlineKeyboardButton(
                    text=option,
                    callback_data=f"answer_{current_question}_{option}"
                )
            ])
        
        # Add cancel button
        keyboard_buttons.append([
            InlineKeyboardButton(
                text="❌ Отменить",
                callback_data=CallbackData.CANCEL_ORDER
            )
        ])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        
        await callback.message.edit_text(
            text=question_text,
            reply_markup=keyboard
        )
    else:
        # Text input question
        await callback.message.edit_text(
            text=f"{question_text}\n\nВведите ваш ответ:",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="❌ Отменить",
                            callback_data=CallbackData.CANCEL_ORDER
                        )
                    ]
                ]
            )
        )
        await state.set_state(OrderStates.WAITING_TEXT_ANSWER)


@router.callback_query(F.text(startswith="answer_"))
async def handle_choice_answer(callback: CallbackQuery, state: FSMContext) -> None:
    """Handle choice answer."""
    user = callback.from_user
    data = await state.get_data()
    current_question = data.get("current_question", 0)
    
    # Parse answer
    parts = callback.data.split("_", 2)
    if len(parts) < 3:
        await callback.answer("Ошибка в данных", show_alert=True)
        return
    
    question_index = int(parts[1])
    answer = parts[2]
    
    # Store answer
    answers = data.get("answers", {})
    answers[CallbackData.ORDER_QUIZ_QUESTIONS[question_index]["id"]] = answer
    await state.update_data(answers=answers, current_question=current_question + 1)
    
    log_user_action(
        user_id=user.id,
        action="quiz_answer",
        question=question_index,
        answer=answer
    )
    
    # Show next question
    await show_question(callback, state)
    await callback.answer()


@router.message(OrderStates.WAITING_TEXT_ANSWER)
async def handle_text_answer(message: Message, state: FSMContext) -> None:
    """Handle text answer."""
    user = message.from_user
    data = await state.get_data()
    current_question = data.get("current_question", 0)
    
    if current_question >= len(CallbackData.ORDER_QUIZ_QUESTIONS):
        await finish_quiz_text(message, state)
        return
    
    question = CallbackData.ORDER_QUIZ_QUESTIONS[current_question]
    answer = message.text
    
    # Store answer
    answers = data.get("answers", {})
    answers[question["id"]] = answer
    await state.update_data(answers=answers, current_question=current_question + 1)
    
    log_user_action(
        user_id=user.id,
        action="quiz_text_answer",
        question=current_question,
        answer=answer
    )
    
    # Show next question
    await show_next_question_text(message, state)


async def show_next_question_text(message: Message, state: FSMContext) -> None:
    """Show next question for text input."""
    data = await state.get_data()
    current_question = data.get("current_question", 0)
    
    if current_question >= len(CallbackData.ORDER_QUIZ_QUESTIONS):
        await finish_quiz_text(message, state)
        return
    
    question = CallbackData.ORDER_QUIZ_QUESTIONS[current_question]
    question_text = f"<b>Вопрос {current_question + 1} из {len(CallbackData.ORDER_QUIZ_QUESTIONS)}</b>\n\n{question['question']}\n\nВведите ваш ответ:"
    
    await message.answer(
        text=question_text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="❌ Отменить",
                        callback_data=CallbackData.CANCEL_ORDER
                    )
                ]
            ]
        )
    )


async def finish_quiz(callback: CallbackQuery, state: FSMContext) -> None:
    """Finish the quiz and save data."""
    user = callback.from_user
    data = await state.get_data()
    answers = data.get("answers", {})
    
    log_user_action(user_id=user.id, action="finish_quiz")
    
    # Create lead data
    lead_data = LeadData(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        service_type=answers.get("service_type", ""),
        budget=answers.get("budget", ""),
        timeline=answers.get("timeline", ""),
        company_name=answers.get("company_name", ""),
        contact_name=answers.get("contact_name", ""),
        contact_phone=answers.get("contact_phone", ""),
        contact_email=answers.get("contact_email", ""),
        additional_info=answers.get("additional_info", "")
    )
    
    try:
        # Save to storage
        storage_service = StorageService()
        await storage_service.save_lead(lead_data)
        
        # Send notification to manager
        notification_service = NotificationService()
        await notification_service.notify_new_lead(lead_data)
        
        success_text = (
            "✅ <b>Заявка успешно отправлена!</b>\n\n"
            "Спасибо за ваш интерес к нашим услугам. "
            "Наш менеджер свяжется с вами в ближайшее время для обсуждения деталей проекта.\n\n"
            "Обычно мы отвечаем в течение 2-4 часов в рабочее время."
        )
        
        await callback.message.edit_text(
            text=success_text,
            reply_markup=get_back_to_menu_keyboard()
        )
        
    except Exception as e:
        logger.error(f"Error saving lead: {e}")
        error_text = (
            "❌ <b>Произошла ошибка при отправке заявки</b>\n\n"
            "Попробуйте еще раз или свяжитесь с нами напрямую через меню 'Связаться с менеджером'."
        )
        
        await callback.message.edit_text(
            text=error_text,
            reply_markup=get_back_to_menu_keyboard()
        )
    
    await state.clear()
    await callback.answer()


async def finish_quiz_text(message: Message, state: FSMContext) -> None:
    """Finish the quiz from text input."""
    user = message.from_user
    data = await state.get_data()
    answers = data.get("answers", {})
    
    log_user_action(user_id=user.id, action="finish_quiz")
    
    # Create lead data
    lead_data = LeadData(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        service_type=answers.get("service_type", ""),
        budget=answers.get("budget", ""),
        timeline=answers.get("timeline", ""),
        company_name=answers.get("company_name", ""),
        contact_name=answers.get("contact_name", ""),
        contact_phone=answers.get("contact_phone", ""),
        contact_email=answers.get("contact_email", ""),
        additional_info=answers.get("additional_info", "")
    )
    
    try:
        # Save to storage
        storage_service = StorageService()
        await storage_service.save_lead(lead_data)
        
        # Send notification to manager
        notification_service = NotificationService()
        await notification_service.notify_new_lead(lead_data)
        
        success_text = (
            "✅ <b>Заявка успешно отправлена!</b>\n\n"
            "Спасибо за ваш интерес к нашим услугам. "
            "Наш менеджер свяжется с вами в ближайшее время для обсуждения деталей проекта.\n\n"
            "Обычно мы отвечаем в течение 2-4 часов в рабочее время."
        )
        
        await message.answer(
            text=success_text,
            reply_markup=get_back_to_menu_keyboard()
        )
        
    except Exception as e:
        logger.error(f"Error saving lead: {e}")
        error_text = (
            "❌ <b>Произошла ошибка при отправке заявки</b>\n\n"
            "Попробуйте еще раз или свяжитесь с нами напрямую через меню 'Связаться с менеджером'."
        )
        
        await message.answer(
            text=error_text,
            reply_markup=get_back_to_menu_keyboard()
        )
    
    await state.clear()


@router.callback_query(F.text(CallbackData.CANCEL_ORDER))
async def cancel_order(callback: CallbackQuery, state: FSMContext) -> None:
    """Cancel order quiz."""
    user = callback.from_user
    log_user_action(user_id=user.id, action="cancel_order")
    
    await state.clear()
    
    cancel_text = (
        "❌ <b>Заказ отменен</b>\n\n"
        "Если у вас есть вопросы, вы можете связаться с нашим менеджером "
        "или вернуться в главное меню."
    )
    
    await callback.message.edit_text(
        text=cancel_text,
        reply_markup=get_back_to_menu_keyboard()
    )
    await callback.answer()

"""
WWWizards Telegram Bot - New Request Router
"""
from aiogram import Router,F
from aiogram.types import CallbackQuery,Message
from aiogram.fsm.context import FSMContext

from app.services.telegram_forward_support import forward_new_request
from app.states.new_order import NewOrderState
from app.constants import CallbackData,COMPANY_INFO
import app.db.requests as rq
from app.keyboards.new_request import get_new_request_keyboard
from app.logging_config import log_user_action
# from app.services.gsheets import add_to_sheet

router = Router()

"""     Main Services Menu      """
@router.callback_query(F.data == CallbackData.NEW_ORDER.value)
async def show_new_request(callback: CallbackQuery,state: FSMContext) -> None:
    """Show New Request menu."""
    user = callback.from_user
    log_user_action(user_id=user.id, action="new_request_stg1")
    await state.set_state(NewOrderState.first_name)
    await callback.message.answer("<b>Введите имя</b>\n\n")
    await callback.answer()


@router.message(NewOrderState.first_name)
async def show_new_request_stg2(message: Message, state:FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(NewOrderState.last_name)
    await message.answer("Введите фамилию")


@router.message(NewOrderState.last_name)
async def show_new_request_stg3(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await state.set_state(NewOrderState.email)
    await message.answer("Введите адрес электронной почты")

@router.message(NewOrderState.email)
async def show_new_request_stg4(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(NewOrderState.description)
    await message.answer("Enter Description")

@router.message(NewOrderState.description)
async def show_new_request_stg5(message: Message, state:FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()

    """ Add user to DB """
    await rq.set_user(message.from_user.id, data["first_name"],data["last_name"], data["email"])
    """ Add request to DB """
    await rq.set_new_request(message.from_user.id, data["first_name"], data["last_name"], data["email"],data["service"], data["description"])
    """ Add request to google sheets """
    # await add_to_sheet(message.from_user.id,data["first_name"], data["last_name"], data["email"],data["service"], data["description"])

    await message.answer(f'Thank you, your request was registered in the system. a representitive will contact you '
                         f'soon\n\nService Requested:{data["service"]}\nName: {data["first_name"]} {data["last_name"]} \nEmail: {data["email"]}\nDescription: {data["description"]}',
                         reply_markup=get_new_request_keyboard())

    """ Send a message to the support/marketing channel"""
    await forward_new_request(data,message)
    await state.clear()


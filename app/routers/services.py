"""
WWWizards Telegram Bot - Services Router
"""
from aiogram import Router, F
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from app.constants import CallbackData
from aiogram.types import CallbackQuery,Message

from loguru import logger

from app.constants import CallbackData
from app.keyboards.services import (get_services_keyboard, get_service_tiers_keyboard, get_submit_request_keyboard,
                                    get_development_design_services_keyboard, get_seo_services_keyboard,
                                    get_marketing_services_keyboard, get_fast_start_services_keyboard,
                                    get_specific_services_keyboard)
from app.logging_config import log_user_action

router = Router()

"""     Main Services Menu      """


@router.message(F.text == CallbackData.MAIN_MENU_SERVICES.value)
async def show_services(message: Message) -> None:
    """Show services menu."""
    user = message.from_user
    log_user_action(user_id=user.id, action="show_services")

    services_text = ("🛠 <b>Выберите категорию услуг</b>\n\n")

    await message.answer(
        text=services_text,
        reply_markup=get_services_keyboard()
    )

"""     Development & Design Services Menu      """


@router.callback_query(F.data == CallbackData.SERVICE_DEVELOPMENT_DESIGN.value)
async def show_development_design_services(callback: CallbackQuery) -> None:
    """Show services menu."""
    user = callback.from_user
    log_user_action(user_id=user.id, action="show_dev_design_services")

    services_text = ("🖌 <b>Разработка и дизайн</b>\n\n"
                     "«Полный цикл создания сайтов: техническая реализация и современный дизайн, который выделяет ваш бизнес.»")

    await callback.message.edit_text(text=services_text, reply_markup=get_development_design_services_keyboard())
    await callback.answer()


"""     Development & Design - Wordpress Services Menu      """
@router.callback_query(F.data == CallbackData.SERVICE_DEVELOPMENT_DESIGN_WORDPRESS.value)
async def show_development_design_wordpress_services(callback: CallbackQuery, state: FSMContext) -> None:
    """Show services menu."""
    service_name = "wordpress"
    user = callback.from_user
    log_user_action(user_id=user.id, action="show_dev_design_wordpress_services")

    services_text = ("🖌 <b>Сайты на WordPress</b>\n\n"
                     "«Наша команда объединяет дизайн и разработку, чтобы создавать сайты на WordPress, которые не только красиво выглядят, но и работают безупречно. Мы разрабатываем уникальные интерфейсы, адаптивные для любых устройств, интегрируем нужные плагины и настраиваем удобную систему управления контентом. Такой сайт легко обновлять, он готов к продвижению и росту вместе с вашим бизнесом.»")

    await callback.message.edit_text(text=services_text,
                                     reply_markup=get_specific_services_keyboard(user.id, service_name))
    await state.update_data(service='wordpress')
    await callback.answer()


"""     Development & Design - NextJS Services Menu      """


@router.callback_query(F.data == CallbackData.SERVICE_DEVELOPMENT_DESIGN_NEXT.value)
async def show_development_design_nextjs_services(callback: CallbackQuery, state: FSMContext) -> None:
    """Show services menu."""
    service_name = "nextjs"
    user = callback.from_user
    log_user_action(user_id=user.id, action="show_dev_design_nextjs_services")

    services_text = ("🖌 <b>Веб-приложения на Next.js</b>\n\n"
                     "«Мы объединяем дизайн и технологии, чтобы создавать веб-решения на Next.js, которые помогают брендам выделяться и расти. Современный стек, серверный рендеринг и оптимизация производительности позволяют вашим сайтам быть максимально быстрыми и удобными. Визуальная часть создаётся под ваши задачи, а функционал расширяется вместе с бизнесом.»")

    await callback.message.edit_text(text=services_text,
                                     reply_markup=get_specific_services_keyboard(user.id, service_name))

    await state.update_data(service='nextjs')
    await callback.answer()


"""     Development & Design - Webflow Services Menu      """
@router.callback_query(F.data == CallbackData.SERVICE_DEVELOPMENT_DESIGN_WEBFLOW.value)
async def show_development_design_webflow_services(callback: CallbackQuery, state: FSMContext) -> None:
    """Show services menu."""
    service_name = "webflow"
    user = callback.from_user
    log_user_action(user_id=user.id, action="show_dev_design_webflow_services")

    services_text = ("🖌 <b>Сайты на Webflow</b>\n\n"
                     "«Мы разрабатываем сайты на Webflow, которые сочетают стильный дизайн, продуманную структуру и простоту управления контентом. Благодаря возможностям платформы, вы получаете современный сайт с гибкими настройками, быстрым временем загрузки и возможностью легко вносить изменения без программиста. Такой сайт идеально подходит для бизнеса, который ценит скорость запуска и высокое качество визуала.»")

    await callback.message.edit_text(text=services_text,
                                     reply_markup=get_specific_services_keyboard(user.id, service_name))

    await state.update_data(service='webflow')
    await callback.answer()


"""     Development & Design - Support Services Menu      """
@router.callback_query(F.data == CallbackData.SERVICE_DEVELOPMENT_DESIGN_SUPPORT.value)
async def show_development_design_support_services(callback: CallbackQuery, state: FSMContext) -> None:
    """Show services menu."""
    service_name = "support"
    user = callback.from_user
    log_user_action(user_id=user.id, action="show_dev_design_uiux_services")

    services_text = ("🖌 <b>Поддержка и сопровождение</b>\n\n"
                     "«Мы обеспечиваем полное техническое сопровождение вашего сайта: обновления, устранение ошибок, настройка безопасности и оптимизация скорости работы. Наша команда следит за стабильностью ресурса, чтобы вы могли сосредоточиться на бизнесе, не думая о технических деталях.»")

    await callback.message.edit_text(text=services_text,
                                     reply_markup=get_specific_services_keyboard(user.id, service_name))

    await state.update_data(service='support')
    await callback.answer()


"""     Development & Design - UIUX Services Menu      """
@router.callback_query(F.data == CallbackData.SERVICE_DEVELOPMENT_DESIGN_UIUX.value)
async def show_development_design_uiux_services(callback: CallbackQuery, state: FSMContext) -> None:
    """Show services menu."""
    service_name = "uiux"
    user = callback.from_user
    log_user_action(user_id=user.id, action="show_dev_design_uiux_services")

    services_text = ("🖌 <b>UI/UX дизайн</b>\n\n"
                     "«Мы проектируем интерфейсы, которые не только красиво выглядят, но и удобны для пользователя. На этапе UI/UX-разработки мы анализируем поведение аудитории, создаём прототипы и тестируем сценарии взаимодействия. Это помогает сделать сайт интуитивным, повысить конверсию и оставить у посетителей положительное впечатление от работы с вашим продуктом.»")

    await callback.message.edit_text(text=services_text,
                                     reply_markup=get_specific_services_keyboard(user.id, service_name))

    await state.update_data(service='uiux')
    await callback.answer()


"""     SEO Services Menu      """


@router.callback_query(F.data == CallbackData.SERVICE_SEO.value)
async def show_seo_services(callback: CallbackQuery) -> None:
    """Show services menu."""
    user = callback.from_user
    log_user_action(user_id=user.id, action="show_dev_design_services")

    services_text = ("🔍 <b>Оптимизация SEO</b>\n\n"
                     "«Улучшаем видимость сайта в поиске и привлекаем новых клиентов»")

    await callback.message.edit_text(text=services_text, reply_markup=get_seo_services_keyboard())
    await callback.answer()


"""     SEO Services Menu - Audit      """
@router.callback_query(F.data == CallbackData.SERVICE_SEO_AUDIT.value)
async def show_seo_audit_services(callback: CallbackQuery, state: FSMContext) -> None:
    """Show services menu."""
    user = callback.from_user
    service_name = "seo_audit"
    log_user_action(user_id=user.id, action="show_seo_audit_services")

    services_text = ("🖌 <b>Разработка и дизайн</b>\n\n"
                     "«Полный цикл создания сайтов: техническая реализация и современный дизайн, который выделяет ваш бизнес.»")

    await callback.message.edit_text(text=services_text,
                                     reply_markup=get_specific_services_keyboard(user.id, service_name))

    await state.update_data(service='seo_audit')
    await callback.answer()


"""     SEO Services Menu - Package      """
@router.callback_query(F.data == CallbackData.SERVICE_SEO_PACKAGE.value)
async def show_seo_package_services(callback: CallbackQuery, state: FSMContext) -> None:
    """Show services menu."""
    service_name = "seo_package"
    user = callback.from_user
    log_user_action(user_id=user.id, action="show_seo_package_services")

    services_text = ("🖌 <b>Разработка и дизайн</b>\n\n"
                     "«Полный цикл создания сайтов: техническая реализация и современный дизайн, который выделяет ваш бизнес.»")

    await callback.message.edit_text(text=services_text,
                                     reply_markup=get_specific_services_keyboard(user.id, service_name))

    await state.update_data(service='seo_package')
    await callback.answer()


"""     SEO Services Menu - Local      """


@router.callback_query(F.data == CallbackData.SERVICE_SEO_LOCAL.value)
async def show_seo_local_services(callback: CallbackQuery, state: FSMContext) -> None:
    """Show services menu."""
    service_name = "seo_local"
    user = callback.from_user
    log_user_action(user_id=user.id, action="show_seo_local_services")

    services_text = ("🖌 <b>Разработка и дизайн</b>\n\n"
                     "«Полный цикл создания сайтов: техническая реализация и современный дизайн, который выделяет ваш бизнес.»")

    await callback.message.edit_text(text=services_text,
                                     reply_markup=get_specific_services_keyboard(user.id, service_name))

    await state.update_data(service='seo_local')
    await callback.answer()


"""     Marketing Services Menu      """


@router.callback_query(F.data == CallbackData.SERVICE_MARKETING.value)
async def show_marketing_services(callback: CallbackQuery) -> None:
    """Show services menu."""
    user = callback.from_user
    log_user_action(user_id=user.id, action="show_dev_design_services")

    services_text = ("📢 <b>Маркетинг и реклама</b>\n\n"
                     "«Продвижение бизнеса через рекламу и маркетинговые инструменты.»")

    await callback.message.edit_text(text=services_text, reply_markup=get_marketing_services_keyboard())
    await callback.answer()


"""     Marketing Services Menu - Google      """


@router.callback_query(F.data == CallbackData.SERVICE_MARKETING_GOOGLE.value)
async def show_marketing_google_services(callback: CallbackQuery, state: FSMContext) -> None:
    """Show services menu."""
    service_name = "marketing_google"
    user = callback.from_user
    log_user_action(user_id=user.id, action="show_marketing_google_services")

    services_text = ("🖌 <b>Разработка и дизайн</b>\n\n"
                     "«Полный цикл создания сайтов: техническая реализация и современный дизайн, который выделяет ваш бизнес.»")

    await callback.message.edit_text(text=services_text,
                                     reply_markup=get_specific_services_keyboard(user.id, service_name))

    await state.update_data(service='marketing_google')
    await callback.answer()


"""     Marketing Services Menu - Yandex      """


@router.callback_query(F.data == CallbackData.SERVICE_MARKETING_YANDEX.value)
async def show_marketing_yandex_services(callback: CallbackQuery, state: FSMContext) -> None:
    """Show services menu."""
    user = callback.from_user
    service_name = "marketing_yandex"
    log_user_action(user_id=user.id, action="show_marketing_yandex_services")

    services_text = ("🖌 <b>Разработка и дизайн</b>\n\n"
                     "«Полный цикл создания сайтов: техническая реализация и современный дизайн, который выделяет ваш бизнес.»")

    await callback.message.edit_text(text=services_text,
                                     reply_markup=get_specific_services_keyboard(user.id, service_name))

    await state.update_data(service='marketing_yandex')
    await callback.answer()


"""     Marketing Services Menu - SMM      """


@router.callback_query(F.data == CallbackData.SERVICE_MARKETING_SMM.value)
async def show_marketing_smm_services(callback: CallbackQuery, state: FSMContext) -> None:
    """Show services menu."""
    service_name = "marketing_smm"
    user = callback.from_user
    log_user_action(user_id=user.id, action="show_marketing_smm_services")

    services_text = ("🖌 <b>Разработка и дизайн</b>\n\n"
                     "«Полный цикл создания сайтов: техническая реализация и современный дизайн, который выделяет ваш бизнес.»")

    await callback.message.edit_text(text=services_text,
                                     reply_markup=get_specific_services_keyboard(user.id, service_name))

    await state.update_data(service='marketing_smm')
    await callback.answer()


"""     Fast Start Services Menu      """


@router.callback_query(F.data == CallbackData.SERVICE_FASTSTART.value)
async def show_faststart_services(callback: CallbackQuery) -> None:
    """Show services menu."""
    user = callback.from_user
    log_user_action(user_id=user.id, action="show_faststart_services")

    services_text = ("🚀 <b>Быстрый запуск</b>\n\n"
                     "«Запускаем проект под ключ максимально быстро — от идеи до первых клиентов.»")

    await callback.message.edit_text(text=services_text, reply_markup=get_fast_start_services_keyboard())
    await callback.answer()


"""     Fast Start Services Menu  - 24h landing    """


@router.callback_query(F.data == CallbackData.SERVICE_FASTSTART_LANDING24.value)
async def show_faststart_landing24_services(callback: CallbackQuery, state: FSMContext) -> None:
    """Show services menu."""
    user = callback.from_user
    service_name = "landing24"
    log_user_action(user_id=user.id, action="show_faststart_landing24_services")

    services_text = ("🖌 <b>Разработка и дизайн</b>\n\n"
                     "«Полный цикл создания сайтов: техническая реализация и современный дизайн, который выделяет ваш бизнес.»")

    await callback.message.edit_text(text=services_text,
                                     reply_markup=get_specific_services_keyboard(user.id, service_name))

    await state.update_data(service='landing24')
    await callback.answer()


"""     Fast Start Services Menu  - Express website    """


@router.callback_query(F.data == CallbackData.SERVICE_FASTSTART_EXPRESS.value)
async def show_faststart_express_services(callback: CallbackQuery, state: FSMContext) -> None:
    """Show services menu."""
    service_name = "faststart_express"
    user = callback.from_user
    log_user_action(user_id=user.id, action="show_faststart_express_services")

    services_text = ("🖌 <b>Разработка и дизайн</b>\n\n"
                     "«Полный цикл создания сайтов: техническая реализация и современный дизайн, который выделяет ваш бизнес.»")

    await callback.message.edit_text(text=services_text,
                                     reply_markup=get_specific_services_keyboard(user.id, service_name))

    await state.update_data(service='express')
    await callback.answer()


"""     Fast Start Services Menu  -  integration    """


@router.callback_query(F.data == CallbackData.SERVICE_FASTSTART_INTEGRATION.value)
async def show_faststart_integration_services(callback: CallbackQuery, state: FSMContext) -> None:
    """Show services menu."""
    service_name = "faststart_integration"
    user = callback.from_user
    log_user_action(user_id=user.id, action="show_faststart_integration_services")

    services_text = ("🖌 <b>Разработка и дизайн</b>\n\n"
                     "«Полный цикл создания сайтов: техническая реализация и современный дизайн, который выделяет ваш бизнес.»")

    await callback.message.edit_text(text=services_text,
                                     reply_markup=get_specific_services_keyboard(user.id, service_name))
    await state.update_data(service='integration')
    await callback.answer()

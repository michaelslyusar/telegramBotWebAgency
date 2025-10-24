"""
WWWizards Telegram Bot - Services Keyboard
"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from app.constants import CallbackData

"""     Main Services Keyboard      """
def get_services_keyboard() -> InlineKeyboardMarkup:
    """Create main services keyboard."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🖌 Разработка и дизайн",
                    callback_data=CallbackData.SERVICE_DEVELOPMENT_DESIGN.value
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎯 Продвижение и SEO",
                    callback_data=CallbackData.SERVICE_SEO.value
                ),
                InlineKeyboardButton(
                    text="📢 Маркетинг и реклама",
                    callback_data=CallbackData.SERVICE_MARKETING.value
                )
            ],
            [
                InlineKeyboardButton(
                    text="🚀 Быстрый запуск",
                    callback_data=CallbackData.SERVICE_FASTSTART.value
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Вернуться",
                    callback_data=CallbackData.BACK_TO_MENU
                )
            ]
        ]
    )
    return keyboard

"""     Development and Design Keyboard      """
def get_development_design_services_keyboard() -> InlineKeyboardMarkup:
    """Create main services keyboard."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Wordpress",
                    callback_data=CallbackData.SERVICE_DEVELOPMENT_DESIGN_WORDPRESS.value
                )
            ],
            [
                InlineKeyboardButton(
                    text="Next.js",
                    callback_data=CallbackData.SERVICE_DEVELOPMENT_DESIGN_NEXT.value
                ),
                InlineKeyboardButton(
                    text="Webflow",
                    callback_data=CallbackData.SERVICE_DEVELOPMENT_DESIGN_WEBFLOW.value
                )
            ],
            [
                InlineKeyboardButton(
                    text="UI/UX дизайн",
                    callback_data=CallbackData.SERVICE_DEVELOPMENT_DESIGN_UIUX.value
                ),InlineKeyboardButton(
                    text="Техподдержка",
                    callback_data=CallbackData.SERVICE_DEVELOPMENT_DESIGN_SUPPORT.value
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Вернуться",
                    callback_data=CallbackData.BACK_TO_MENU
                )
            ]
        ]
    )
    return keyboard


"""     SEO Keyboard      """
def get_seo_services_keyboard() -> InlineKeyboardMarkup:
    """Create main services keyboard."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="SEO аудит",
                    callback_data=CallbackData.SERVICE_SEO_AUDIT.value
                )
            ],
            [
                InlineKeyboardButton(
                    text="Комплексное продвижение",
                    callback_data=CallbackData.SERVICE_SEO_PACKAGE.value
                ),
                InlineKeyboardButton(
                    text="Локальное SEO",
                    callback_data=CallbackData.SERVICE_SEO_LOCAL.value
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Вернуться",
                    callback_data=CallbackData.BACK_TO_MENU
                )
            ]
        ]
    )
    return keyboard

"""     Marketing Keyboard      """
def get_marketing_services_keyboard() -> InlineKeyboardMarkup:
    """Create main services keyboard."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Google Ads",
                    callback_data=CallbackData.SERVICE_MARKETING_GOOGLE.value
                )
            ],
            [
                InlineKeyboardButton(
                    text="Яндекс Директ",
                    callback_data=CallbackData.SERVICE_MARKETING_YANDEX.value
                ),
                InlineKeyboardButton(
                    text="SMM",
                    callback_data=CallbackData.SERVICE_MARKETING_SMM.value
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Вернуться",
                    callback_data=CallbackData.BACK_TO_MENU
                )
            ]
        ]
    )
    return keyboard

"""     Fast Start Keyboard      """
def get_fast_start_services_keyboard() -> InlineKeyboardMarkup:
    """Create main services keyboard."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Лендинг за 24 часа",
                    callback_data=CallbackData.SERVICE_FASTSTART_LANDING24.value
                )
            ],
            [
                InlineKeyboardButton(
                    text="Экспресс-сайт",
                    callback_data=CallbackData.SERVICE_FASTSTART_EXPRESS.value
                ),
                InlineKeyboardButton(
                    text="Быстрая интеграция",
                    callback_data=CallbackData.SERVICE_FASTSTART_INTEGRATION.value
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Вернуться",
                    callback_data=CallbackData.BACK_TO_MENU
                )
            ]
        ]
    )
    return keyboard


"""     Services - Specific Keyboard      """
def get_specific_services_keyboard(user_id,service) -> InlineKeyboardMarkup:
    url = f"https://hillagagusil.beget.app/callback?service={service}&uid={user_id}&source=tgbot"
    print(url)
    """Create main services keyboard."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Оставить заявку",
                    web_app=WebAppInfo(url=url)
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Вернуться",
                    callback_data=CallbackData.BACK_TO_MENU
                )
            ]
        ]
    )
    return keyboard






def get_service_tiers_keyboard(service_key: str) -> InlineKeyboardMarkup:
    """Create service tiers keyboard for specific service."""
    service = CallbackData.SERVICES.get(service_key)
    if not service:
        return get_services_keyboard()
    
    keyboard_buttons = []
    for tier_key, tier_data in service["services"].items():
        keyboard_buttons.append([
            InlineKeyboardButton(
                text=f"{tier_data['name']} - {tier_data['price']}",
                callback_data=f"{service_key}_{tier_key}"
            )
        ])
    
    # Add back button
    keyboard_buttons.append([
        InlineKeyboardButton(
            text="⬅️ Назад к услугам",
            callback_data=CallbackData.BACK_TO_SERVICES
        )
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    return keyboard


def get_submit_request_keyboard() -> InlineKeyboardMarkup:
    """Create submit request keyboard."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📝 Подать заявку",
                    callback_data=CallbackData.SUBMIT_REQUEST
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад к услугам",
                    callback_data=CallbackData.BACK_TO_SERVICES
                )
            ]
        ]
    )
    return keyboard


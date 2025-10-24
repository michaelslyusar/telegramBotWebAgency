from app.constants import COMPANY_INFO

async def forward_new_request(data,message):
    """ Send a message to the support/marketing channel"""
    text = (
        f"📥 New registration:\n\n"
        f"✉️ {data['service']}\n"
        f"👤 {data['first_name']} {data['last_name']}\n"
        f"✉️ {data['email']}\n"
        f"✉️ {data['description']}\n"
        f"🆔 Telegram ID: {message.from_user.id}"
    )
    await message.bot.send_message(COMPANY_INFO["tg_support_channel_id"], text)
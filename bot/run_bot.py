from bot import bot
from core.settings import settings


async def set_telegram_webhook():
    response = bot.set_webhook(url=settings.app_config__telegram__webhook_url)
    if response:
        print('Работает по')
    else:
        print('по не работает')
from bot import bot
from core import settings


async def set_telegram_webhook():
    response = await bot.set_webhook(url=settings.tg.webhook_url)
    if response:
        print('По запустил бота на вебхуков')
    else:
        print('По не запустил вебхуки')
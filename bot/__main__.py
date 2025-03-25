from bot.run_bot import set_telegram_webhook
import asyncio
from bot.mainhandlers import router
from bot import dp
dp.include_router(router)


def run_webhook():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(set_telegram_webhook())
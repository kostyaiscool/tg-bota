import asyncio

from aiogram import Bot
from aiogram.types import BotCommand
from aiogram_dialog import setup_dialogs
from sqlalchemy.util import await_only

from api.utils.set_telegram_webhook import set_telegram_webhook, delete_telegram_webhook
from bot import dispatcher, bot
from bot.dialogs import dialog
from core import settings, RunningMode, logger
from bot.handlers.messages import router as messages_router

dispatcher.include_router(messages_router)
dispatcher.include_router(dialog)
setup_dialogs(dispatcher)

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/menu", description="Отображает главное меню"),
        BotCommand(command="/clear", description="Круче чем Танос"),
    ]
    await bot.set_my_commands(commands)
async def run_polling() -> None:
    await set_commands(bot)
    await delete_telegram_webhook()
    await dispatcher.start_polling(bot)
    logger.info("Bot started in long pooling mode")

async def run_webhook() -> None:
    await set_commands(bot)
    await set_telegram_webhook()
    logger.info("Bot started in Webhook mode")

def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    if settings.telegram.running_mode == RunningMode.LONG_POLLING:
        loop.run_until_complete(run_polling())
    elif settings.telegram.running_mode == RunningMode.WEBHOOK:
        loop.run_until_complete(run_webhook())
    else:
        logger.error("Unknown running mode")
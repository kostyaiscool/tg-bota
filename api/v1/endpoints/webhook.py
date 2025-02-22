from fastapi import APIRouter, Request
from aiogram.types import Update

from bot import bot, dispatcher
from core import settings

router = APIRouter(tags=["webhooks"])


@router.post(settings.telegram.webhook_path)
async def telegram_webhook(request: Request):
    update = Update(**await request.json())
    await dispatcher.feed_update(bot=bot, update=update)

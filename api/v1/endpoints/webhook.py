from fastapi import APIRouter, Request
from aiogram.types import Update

from bot import bot, dp
from core import settings

router = APIRouter(tags=["webhooks"])


@router.post(settings.app_config__telegram__webhook_path)
async def telegram_webhook(request: Request):
    update = Update(**await request.json())
    await dp.feed_update(bot=bot, update=update)


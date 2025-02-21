from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from core import settings

bot = Bot(
    token=settings.telegram.token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dispatcher = Dispatcher()
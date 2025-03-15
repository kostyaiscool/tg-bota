from aiogram import Bot, Dispatcher
from core.settings import settings


bot = Bot(token=settings.app_config__telegram__token)
dp = Dispatcher()

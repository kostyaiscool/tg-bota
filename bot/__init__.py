from aiogram import Bot, Dispatcher
from core.settings import settings


bot = Bot(token=settings.tg.token)
dp = Dispatcher()

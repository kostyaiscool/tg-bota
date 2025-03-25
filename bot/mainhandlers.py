from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from bot import bot
from schemas.user import TelegramUser

router = Router()
@router.message(Command(commands=['start', 'help']))
async def route(message: Message):
    # await message.answer('Здарова')
    if message.from_user is None:
        return None
    user_data = TelegramUser(
        id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        language_code=message.from_user.language_code,
        is_premium=message.from_user.is_premium or False,
        is_bot=message.from_user.is_bot
    )
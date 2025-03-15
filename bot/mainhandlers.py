from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from bot import bot

router = Router()
@router.message(Command(commands=['start', 'help']))
async def route(message: Message):
    await message.answer('Здарова')
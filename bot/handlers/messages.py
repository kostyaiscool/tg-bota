from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import aiohttp
from core import logger
from schemas.user import TelegramUser

router = Router()

@router.message(Command(commands=["start"]))
async def start_command(message: Message):
    """Обробник команди /start."""
    if message.from_user is None:
        return

    # Створюємо об'єкт Pydantic схеми
    user_data = TelegramUser(
        id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        language_code=message.from_user.language_code,
        is_premium=message.from_user.is_premium or False,
        is_bot=message.from_user.is_bot
    )

    # Відправляємо POST-запит до FastAPI ендпоінту
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                "http://localhost:8000/add_user",
                json=user_data.dict()
            ) as response:
                if response.status != 200:
                    logger.error(f"Failed to add user: {await response.text()}")
                    await message.answer("Щось пішло не так. Спробуйте ще раз пізніше.")
                    return

                # Отримуємо відповідь від API
                response_data = await response.json()
                is_new_user = response_data["is_new_user"]

                # Відправляємо різні повідомлення в залежності від статусу
                if is_new_user:
                    await message.answer(f"Привіт, {message.from_user.first_name}! Ти успішно зареєстрований у базі. 🚀")
                else:
                    await message.answer(f"Раді знову тебе бачити, {message.from_user.first_name}! 🎉")
        except Exception as e:
            logger.error(f"Error while adding user: {e}")
            await message.answer("Щось пішло не так. Спробуйте ще раз пізніше.")
import asyncio

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message
import aiohttp
from aiogram_dialog import StartMode, DialogManager

from bot import bot
from bot.dialogs.v2.states import Wiki
# from bot.dialogs.states import Wiki, Creation
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


@router.message(Command(commands=["menu"]))
async def menu_command(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(Wiki.main, mode=StartMode.RESET_STACK)
    # await dialog_manager.start(Creation.create_name)

@router.message(Command("clear"))
async def clear_chat(message: Message, bot: Bot):
    chat_id = message.chat.id
    from_id = message.message_id
    chat_type = message.chat.type

    deleted = 0
    limit = 100

    # Временное сообщение
    notice = await message.answer("🧹 Очищаю сообщения...")

    for msg_id in range(from_id, from_id - limit, -1):
        try:
            msg = await bot.forward_message(chat_id=chat_id, from_chat_id=chat_id, message_id=msg_id)
            await bot.delete_message(chat_id, msg.message_id)  # Удаляем копию (если удалось)
            await bot.delete_message(chat_id, msg_id)          # Пытаемся удалить оригинал
            deleted += 1
            await asyncio.sleep(0.05)
        except Exception:
            # В личке Telegram не даст удалить чужие сообщения (и старые тоже иногда)
            if chat_type == "private":
                try:
                    # Получаем сообщение и удаляем, если оно от бота
                    original = await bot.get_chat_member(chat_id, bot.id)
                    msg = await bot.get_chat_message(chat_id, msg_id)
                    if msg.from_user.id == bot.id:
                        await bot.delete_message(chat_id, msg_id)
                        deleted += 1
                except:
                    pass
            continue

    # Пытаемся удалить саму команду и уведомление
    try:
        await bot.delete_message(chat_id, message.message_id)
        await bot.delete_message(chat_id, notice.message_id)
    except:
        pass

    # Или отправляем новое сообщение
    await message.answer(f"✅ Удалено {deleted} сообщений.")
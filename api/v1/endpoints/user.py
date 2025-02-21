from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import db_helper
from db.crud.user import TelegramUserCRUD
from schemas.user import TelegramUser

router = APIRouter(tags=["users"])


@router.post("/add_user")
async def add_user(user_data: TelegramUser, db: AsyncSession = Depends(db_helper.session_getter)):
    user, is_new_user = await TelegramUserCRUD.create_or_update_user(db, user_data)
    return {"user": user, "is_new_user": is_new_user}

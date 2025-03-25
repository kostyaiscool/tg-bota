from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import db_help
from db.crud.user import TelegramUserCRUD
from schemas.user import TelegramUser

router = APIRouter(tags=["users"])


@router.post("/add_user")
async def add_user(user_data: TelegramUser, db: AsyncSession = Depends(db_help.session_get)):
    user = await TelegramUserCRUD.create_or_update(db, user_data)
    return {"user": user}
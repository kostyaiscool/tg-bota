from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import db_helper
from db.crud.categories import CategoryCRUD
from schemas.categories import Categories

router = APIRouter(tags=["categories"])


@router.post("/add_category")
async def add_category(category_data: Categories, db: AsyncSession = Depends(db_helper.session_get)):
    category = await CategoryCRUD.create_or_update(db, category_data)
    return {"category": category}
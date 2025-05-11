from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import db_helper
from db.crud.pages import PageCRUD
from schemas.pages import Pages

router = APIRouter(tags=["pages"])


@router.post("/add_page")
async def add_page(page_data: Pages, db: AsyncSession = Depends(db_helper.session_get)):
    page = await PageCRUD.create_or_update(db, page_data)
    return {"page": page}
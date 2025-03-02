from contextlib import asynccontextmanager
from core.settings import settings
from fastapi import FastAPI
import uvicorn
from db.db import db_help

@asynccontextmanager
async def lifespan(app):
    await db_help.init_db()
    print('300 - полный век програмиста')
    yield
    await db_help.dispose()
    print('Скажи клей')
app: FastAPI = FastAPI(lifespan=lifespan)
if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)


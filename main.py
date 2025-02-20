from core.settings import settings
from fastapi import FastAPI
import uvicorn
from db.db import db_help


async def lifespan(app):
    print('300 - полный век програмиста')
    yield
    db_help.dispose()
    print('Скажи клей')
app: FastAPI = FastAPI()
if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)

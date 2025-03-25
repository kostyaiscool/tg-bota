from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from db.db import db_help
from bot.__main__ import run_webhook
import threading
from api.v1.endpoints.webhook import router as webhook_router
from api.v1.endpoints.user import router as user_router

@asynccontextmanager
async def lifespan(app):
    await db_help.init_db()
    print('300 - полный век програмиста')
    yield
    await db_help.dispose()
    print('Скажи клей')
app: FastAPI = FastAPI(lifespan=lifespan)
app.include_router(webhook_router)
app.include_router(user_router)
if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_webhook, daemon=True)
    bot_thread.start()
    uvicorn.run('main:app', reload=True)
    bot_thread.join()
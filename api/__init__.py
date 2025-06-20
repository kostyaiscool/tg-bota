from fastapi import FastAPI
from sqladmin import Admin
from contextlib import asynccontextmanager

from db.database import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
   await db_helper.init_db()
   yield
   await db_helper.dispose()


app = FastAPI(title="Backend API", version="1.0", lifespan=lifespan)

admin_app = Admin(app, db_helper.engine)
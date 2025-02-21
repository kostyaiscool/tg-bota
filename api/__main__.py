import uvicorn

from core import settings
from api import app
from api.v1.endpoints.webhook import router as webhook_router
from api.v1.endpoints.user import router as user_router

app.include_router(webhook_router)
app.include_router(user_router)

def run_api():
    uvicorn.run(
      app="api:app",
      host=settings.run.host,
      port=settings.run.port,
      reload=settings.run.reload,
    )
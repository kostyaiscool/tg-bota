import uvicorn

from api.admin.models import UserAdmin
from core import settings
from api import app, admin_app
from api.v1.endpoints.webhook import router as webhook_router
from api.v1.endpoints.user import router as user_router

app.include_router(webhook_router)
app.include_router(user_router)
admin_app.add_view(UserAdmin)

for route in app.routes:
    print(route.path, route.name)


def run_api():
    uvicorn.run(
      app="api:app",
      host=settings.run.host,
      port=settings.run.port,
      reload=settings.run.reload,
    )
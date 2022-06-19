from fastapi import APIRouter, FastAPI

from shifts.app.api.api_v1.api import api_router
from shifts.app.core.config import settings

app = FastAPI(title="Shifts API", openapi_url="/openapi.json")

root_router = APIRouter()
app = FastAPI(title="Recipe API")

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)

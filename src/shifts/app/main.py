from fastapi import APIRouter, FastAPI

from app.api.api_v1.api import api_router
from app.core.config import settings

root_router = APIRouter()
app = FastAPI(title="Shifts API", openapi_url="/openapi.json")


@root_router.get("/")
async def root():
    return {"message": ""}


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)

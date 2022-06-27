from app.api.api_v1.endpoints import auth, manager, shift, worker
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(worker.router, prefix="/workers", tags=["workers"])
api_router.include_router(manager.router, prefix="/managers", tags=["managers"])
api_router.include_router(shift.router, prefix="/shifts", tags=["shifts"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

from fastapi import APIRouter

from shifts.app.api.api_v1.endpoints import manager, shift, worker

api_router = APIRouter()
api_router.include_router(worker.router, prefix="/workers", tags=["workers"])
api_router.include_router(manager.router, prefix="/managers", tags=["managers"])
api_router.include_router(shift.router, prefix="/shifts", tags=["shifts"])

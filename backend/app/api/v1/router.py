from fastapi import APIRouter

from app.api.v1.endpoints import auth, health, tasks, users

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_v1_router.include_router(health.router, prefix="/health", tags=["health"])
api_v1_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_v1_router.include_router(users.router, prefix="/users", tags=["users"])

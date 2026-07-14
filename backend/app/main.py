from fastapi import FastAPI

from app.api.router import api_router
from app.api.v1.router import api_v1_router
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME, version="1.0.0")
app.include_router(api_router)
app.include_router(api_v1_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"system": "Quan ly Cong viec Dang uy xa Ea Kiet", "version": "1.0.0", "status": "running"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

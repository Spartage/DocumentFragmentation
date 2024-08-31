from fastapi import APIRouter
from app.api.endpoints import fragment

fragment_router = APIRouter()

fragment_router.include_router(fragment.router, prefix="/fragments", tags=["Fragments"])
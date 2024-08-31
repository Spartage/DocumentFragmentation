from fastapi import APIRouter
from app.api.fragment_router import fragment_router

router = APIRouter()

# Incluir todos los routers categorizados
router.include_router(fragment_router)
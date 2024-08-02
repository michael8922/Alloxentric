from fastapi import APIRouter
from app.resources.example import router as resources_router
from app.resources.registromedico import router as resources_router2

router = APIRouter()
router.include_router(resources_router, prefix="/example", tags=["example"])
router.include_router(resources_router2, prefix="/medicos", tags=["medicos"])
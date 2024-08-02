from fastapi import APIRouter
from app.resources.example import router as resources_router
from app.resources.listarDoctores import router as resources_router_doctores
from app.resources.anularCita import router as resources_router_anular
from app.resources.chatclient import router as resources_router_chat

router = APIRouter()
router.include_router(resources_router, prefix="/example", tags=["example"])
router.include_router(resources_router_doctores, prefix="/listarDoctores", tags=["listarDoctores"])
router.include_router(resources_router_anular, prefix="/anularCitas", tags=["anularCitas"])
router.include_router(resources_router_chat, prefix="/chat", tags=["chat"])
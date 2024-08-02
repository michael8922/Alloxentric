from fastapi import APIRouter
from app.resources.example import router as resources_router
# from app.resources.registromedico import router as resources_router2
from app.resources.config_medico import router as resources_router3
#from app.resources.canal_confirmacion import router as canal_confirmacion_medico

router = APIRouter()
router.include_router(resources_router, prefix="/example", tags=["example"])
# router.include_router(resources_router2, prefix="/medicos", tags=["medicos"])
router.include_router(resources_router3, prefix="/conf_medicos", tags=["conf_medicos"])
#router.include_router(canal_confirmacion_medico, prefix="/confirma_medicos", tags=["confirma_medicos"])

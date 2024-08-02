from fastapi import APIRouter
from app.resources.example import router as resources_router
from app.resources.region import router as region_router
from app.resources.comuna import router as comuna_router
from app.resources.hora import router as hora_router
from app.resources.centro_medico import router as centro_medico_router
from app.resources.especialidad import router as especialidad
from app.resources.prevision import router as prestacion_router

router = APIRouter()
router.include_router(resources_router, prefix="/example", tags=["example"])
router.include_router(region_router, prefix="/regiones", tags=["regiones"])
router.include_router(comuna_router, prefix="/comunas", tags=["comunas"])
router.include_router(hora_router, prefix="/horas", tags=["horas"])
router.include_router(centro_medico_router, prefix="/centros", tags=["centros"])
router.include_router(especialidad, prefix="/especialidades", tags=["especialidades"])
router.include_router(prestacion_router, prefix="/previsiones", tags=["previsiones"])


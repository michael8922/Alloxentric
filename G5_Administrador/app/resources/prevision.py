import logging
from typing import List
from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.model import Prevision


from app.auth import get_db


router = APIRouter(
    tags=["previsiones"],
    responses={404: {"description": "Not found"}},
)

@router.get("/prevision")
async def get_all_prestacion(db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))) -> List[Prevision]:
    """Endpoint para obtener todos los datos de Prestaciones de la base de datos"""
    logging.info("get all previsiones")
    try:
        previsiones = await db["prevision"].find().to_list(length=100)
        if previsiones is None:
            previsiones = []
    except Exception as err:
        logging.error(err)
    return previsiones
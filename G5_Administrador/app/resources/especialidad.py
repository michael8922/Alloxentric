import logging
from typing import List
from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.model import Especialidad


from app.auth import get_db

router = APIRouter(
    tags=["especialidad"],
    responses={404: {"description": "Not found"}},
)

@router.get("/especialidad")
async def get_all_regions(db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))) -> List[Especialidad]:
    """Endpoint para obtener todos los datos de tipo Region de la base de datos"""
    logging.info("get all specialty")
    try:
        especialidades = await db["especialidad"].find().to_list(length=100)
        if especialidades is None:
            especialidades = []
    except Exception as err:
        logging.error(err)
    return especialidades
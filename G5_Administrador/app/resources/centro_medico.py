import logging
from typing import List
from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.model import CentroMedico


from app.auth import get_db


router = APIRouter(
    tags=["centros"],
    responses={404: {"description": "Not found"}},
)

@router.post("/centro_medico")
async def post_centro_medico(centro_medico: CentroMedico, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="POST"))):
    """Endpoint para crear un dato de tipo CentroMedico en la base de datos"""
    data = jsonable_encoder(centro_medico)
    logging.info(f"post example with: {centro_medico}")

    # Verificar si la comuna existe
    db_comuna = await db["comuna"].find_one({"name_comuna": centro_medico.comuna.name_comuna})
    if not db_comuna:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Comuna not found"})

    # Verificar si la region existe
    db_region = await db["region"].find_one({"name_region": centro_medico.comuna.region.name_region})
    if not db_region:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Region not found"})

    db_data = await db["centro_medico"].find_one({"name_centro_medico": centro_medico.name_centro_medico})
    if db_data:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"message": "Data already exists"})

    new_data = await db["centro_medico"].insert_one(data)
    return f"{new_data.inserted_id}"


@router.delete("/centro_medico/{centro_medico_id}")
async def delete_centro_medico(centro_medico_id: str, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="DELETE"))):
    """Endpoint para eliminar un dato de tipo CentroMedico de la base de datos por ID"""
    delete_result = await db["centro_medico"].delete_one({"_id": centro_medico_id})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Data deleted successfully"})
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Data not found"})

@router.get("/centro_medico")
async def get_all_centros_medicos(db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))) -> List[CentroMedico]:
    """Endpoint para obtener todos los datos de tipo CentroMedico de la base de datos"""
    logging.info("get all centros medicos")
    try:
        centros_medicos = await db["centro_medico"].find().to_list(length=100)
        if centros_medicos is None:
            centros_medicos = []
    except Exception as err:
        logging.error(err)
    return centros_medicos


@router.get("/centro_medico/{centro_medico_id}")
async def get_centro_medico(centro_medico_id: str, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))):
    """Endpoint para obtener un dato de tipo CentroMedico de la base de datos por ID"""
    centro_medico = await db["centro_medico"].find_one({"_id": centro_medico_id})
    if centro_medico:
        return centro_medico
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Data not found"})
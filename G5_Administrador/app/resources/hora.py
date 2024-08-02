import logging
from typing import List
from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.model import Hora


from app.auth import get_db


router = APIRouter(
    tags=["horas"],
    responses={404: {"description": "Not found"}},
)

@router.post("/hora")
async def post_hora(hora: Hora, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="POST"))):
    """Endpoint para crear un dato de tipo Hora en la base de datos"""
    data = jsonable_encoder(hora)
    logging.info(f"post example with: {hora}")

    # Agregar aquí la lógica específica para el modelo de Hora, si es necesario

    new_data = await db["hora"].insert_one(data)
    return f"{new_data.inserted_id}"



@router.delete("/hora/{hora_id}")
async def delete_hora(hora_id: str, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="DELETE"))):
    """Endpoint para eliminar un dato de tipo Hora de la base de datos por ID"""
    delete_result = await db["hora"].delete_one({"_id": hora_id})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Data deleted successfully"})
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Data not found"})



@router.get("/hora")
async def get_all_horas(db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))) -> List[Hora]:
    """Endpoint para obtener todos los datos de tipo Hora de la base de datos"""
    logging.info("get all horas")
    try:
        horas = await db["hora"].find().to_list(length=100)
        if horas is None:
            horas = []
    except Exception as err:
        logging.error(err)
    return horas



@router.get("/hora/{hora_id}")
async def get_hora(hora_id: str, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))):
    """Endpoint para obtener un dato de tipo Hora de la base de datos por ID"""
    hora = await db["hora"].find_one({"_id": hora_id})
    if hora:
        return hora
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Data not found"})
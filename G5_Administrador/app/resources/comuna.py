import logging
from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.model import Comuna, CentroMedico


from app.auth import get_db


router = APIRouter(
    tags=["comunas"],
    responses={404: {"description": "Not found"}},
)

@router.post("/comuna")
async def post_comuna(comuna: Comuna, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="POST"))):
    """Endpoint para crear un dato de tipo Comuna en la base de datos"""
    data = jsonable_encoder(comuna)
    logging.info(f"post example with: {comuna}")

    # Verificar si la región existe
    db_region = await db["region"].find_one({"name_region": comuna.region.name_region})
    if not db_region:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Region not found"})

    db_data = await db["comuna"].find_one({"name_comuna": comuna.name_comuna})
    if db_data:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"message": "Data already exists"})

    new_data = await db["comuna"].insert_one(data)
    return f"{new_data.inserted_id}"



@router.delete("/comuna/{comuna_id}")
async def delete_comuna(comuna_id: str, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="DELETE"))):
    """Endpoint para eliminar un dato de tipo Comuna de la base de datos por ID"""
    try:
        # Eliminar la comuna
        delete_comuna_result = await db["comuna"].delete_one({"_id": comuna_id})

        # Eliminar los centros médicos asociados a la comuna eliminada
        await db["centro_medico"].delete_many({"comuna._id": comuna_id})

        if delete_comuna_result.deleted_count == 1:
            return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Data deleted successfully"})
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    


@router.get("/comuna", response_model=List[Comuna])
async def get_all_comunas(db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))) -> List[Comuna]:
    """Endpoint para obtener todos los datos de tipo Comuna de la base de datos"""
    try:
        logging.info("get all comunas")
        comunas = await db["comuna"].find().to_list(length=100)
        if not comunas:
            return []
        return comunas
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")





@router.get("/comuna/{comuna_id}")
async def get_comuna(comuna_id: str, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))):
    """Endpoint para obtener un dato de tipo Comuna de la base de datos por ID"""
    comuna = await db["comuna"].find_one({"_id": comuna_id})
    if comuna:
        return comuna
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Data not found"})


@router.get("/comuna/region/{name_region}", response_model=List[Comuna])
async def get_comunas_by_region(name_region: str, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))) -> List[Comuna]:
    """Endpoint para obtener todas las comunas asociadas a una región específica"""
    try:
        logging.info(f"Get all comunas for region with name: {name_region}")

        comunas = await db["comuna"].find({"region.name_region": name_region}).to_list(length=100)
        if not comunas:
            return []
        return comunas
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

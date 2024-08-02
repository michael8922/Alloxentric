import logging
from typing import List
from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.model import Region


from app.auth import get_db


router = APIRouter(
    tags=["regiones"],
    responses={404: {"description": "Not found"}},
)


@router.post("/region")
async def post_region(region: Region, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="POST"))):
    """Endpoint para crear un dato de tipo Region en la base de datos"""
    data = jsonable_encoder(region)
    logging.info(f"post example with: {region}")

    db_data = await db["region"].find_one({"name_region": region.name_region})
    if db_data:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"message": "Data already exists"})

    new_data = await db["region"].insert_one(data)
    return f"{new_data.inserted_id}"



@router.delete("/region/{region_id}")
async def delete_region(region_id: str, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="DELETE"))):
    """Endpoint para eliminar un dato de tipo Region de la base de datos por ID"""
    # Eliminar la región
    delete_region_result = await db["region"].delete_one({"_id": region_id})

    # Eliminar todas las comunas asociadas a la región eliminada
    delete_comunas_result = await db["comuna"].delete_many({"region._id": region_id})

    # Eliminar todos los centros médicos asociados a las comunas eliminadas
    if delete_comunas_result.deleted_count > 0:
        comunas_deleted_ids = [comuna_id["_id"] for comuna_id in delete_comunas_result.deleted_ids]
        await db["centro_medico"].delete_many({"comuna._id": {"$in": comunas_deleted_ids}})

    if delete_region_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Data deleted successfully"})
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Data not found"})


@router.get("/region")
async def get_all_regions(db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))) -> List[Region]:
    """Endpoint para obtener todos los datos de tipo Region de la base de datos"""
    logging.info("get all regions")
    try:
        regions = await db["region"].find().to_list(length=100)
        if regions is None:
            regions = []
    except Exception as err:
        logging.error(err)
    return regions

@router.get("/region/{region_id}")
async def get_region(region_id: str, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))):
    """Endpoint para obtener un dato de tipo Region de la base de datos por ID"""
    region = await db["region"].find_one({"_id": region_id})
    if region:
        return region
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Data not found"})
import logging
from typing import List
from fastapi import APIRouter, status, Depends,HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.model import Medico

from app.auth import get_db


from itertools import cycle


router = APIRouter()

router = APIRouter(
    tags=["medicos"],
    responses={404: {"description": "Not found"}},
)



@router.post("/medico")
async def post_medico(medico: Medico, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="POST"))):
    """Endpoint para crear un dato en la base de datos del Medico"""

    # Validar campos no nulos
    if not all([medico.rut, medico.nombre, medico.apellido, medico.correo, medico.telefono, medico.especialidad, medico.prestacion, medico.centromedisco]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ninguno de los campos puede ser nulo")
    # Validar el RUT
    if not validar_rut(medico.rut):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="RUT inválido")
        # Validar el dominio del correo electrónico
    
    # Convertir el modelo a un diccionario
    medico_dict = jsonable_encoder(medico)
    logging.info(f"post medico with: {medico_dict}")
    medico_dict = dict(medico)
   

    # Buscar si el dato ya existe
    db_data = await db["medico"].find_one({"rut": medico.rut})
    if db_data:
        # Si el dato ya existe, retornar un error
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Data already exists")

    # Si el dato no existe, crearlo con sus fechas de creación
    medico_dict['created_at'] = datetime.now()
    medico_dict['updated_at'] = datetime.now()
    new_data = await db["medico"].insert_one(medico_dict)

    # Retornar el id del nuevo dato
    return str(new_data.inserted_id)


@router.get("/medico")
async def get_medico(rut: str = None, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))) -> List[Medico] | Medico:
    """Endpoint para obtener un dato de la base de datos"""
    # Buscar el dato por el nombre
    if rut is None:
        logging.info("get all medicos")
        try:
            data = await db["medico"].find().to_list(length=100)
            if data is None:
                data = []
        except Exception as err:
            logging.error(err)
        return data

    logging.info(f"get medico with rut: {rut}")
    data = await db["medico"].find_one({"rut": rut})

    if data:
        # Si el dato existe, retornarlo
        return data

    else:
        # Si el dato no existe, retornar un error
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, 
                            content={"message": "Data not found"})
    
@router.delete("/medico/{rut}")
async def delete_medico(rut: str, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="DELETE"))):
    """Endpoint para eliminar un medico de la base de datos por RUT"""
    logging.info(f"Eliminando medico con RUT: {rut}")

    # Verificar si existe el Medico con el RUT dado
    medico = await db["medico"].find_one({"rut": rut})
    if not medico:
        raise HTTPException(status_code=404, detail="Medico no encontrado")

    # Eliminar el medico
    await db["medico"].delete_one({"rut": rut})

    # Retornar un mensaje de éxito
    return {"message": f"Medico con RUT: {rut} ha sido eliminado exitosamente."}

@router.put("/medico/{rut}")
async def put_medico_by_rut(rut: str, data: dict, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="PUT"))):
    """Endpoint para actualizar un medico en la base de datos por RUT"""
    # Verificar si existe el medico con el RUT dado
    medico = await db["medico"].find_one({"rut": rut})
    if not medico:
        raise HTTPException(status_code=404, detail="Medico no encontrado")

    # Actualizar solo los campos permitidos
    allowed_fields = {"nombre", "apellido", "correo"}
    updated_data = {key: value for key, value in data.items() if key in allowed_fields}

    # Verificar si se han proporcionado campos válidos para la actualización
    if not updated_data:
        raise HTTPException(status_code=400, detail="No se proporcionaron campos válidos para la actualización.")

    # Actualizar el dato
    updated_data['updated_at'] = datetime.now()

    # Realizar la actualización en la base de datos
    await db["medico"].update_one({"rut": rut}, {"$set": updated_data})

    return {"message": f"Medico con RUT: {rut} ha sido actualizado exitosamente."}

@router.get("/medicos", response_model=List[Medico])
async def get_medicos(db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))):
    """Endpoint para obtener todos los medicos de la base de datos"""
    # Buscar todos los medicos
    logging.info("Obteniendo todos los medicos")
    try:
        medicos = await db["medico"].find().to_list(length=100)
        if not medicos:
            medicos = []
    except Exception as err:
        logging.error(err)
        raise HTTPException(status_code=500, detail="Error interno del servidor")

    return medicos

# Función de validación de RUT
def validar_rut(rut):
    rut = rut.replace(".", "").upper()
    rut = rut.replace("-", "")
    aux = rut[:-1]
    dv = rut[-1]

    revertido = map(int, reversed(str(aux)))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(revertido, factors))
    res = (-s) % 11

    if str(res) == dv:
        return True
    elif dv == "K" and res == 10:
        return True
    else:
        return False


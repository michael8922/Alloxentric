import logging
from typing import List
from fastapi import APIRouter, status, Depends,HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.model import Paciente

from app.auth import get_db


from itertools import cycle


router = APIRouter()

router = APIRouter(
    tags=["pacientes"],
    responses={404: {"description": "Not found"}},
)



@router.post("/paciente")
async def post_paciente(paciente: Paciente, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="POST"))):
    """Endpoint para crear un dato en la base de datos"""

    # Validar campos no nulos
    if not all([paciente.rut, paciente.nombre, paciente.apellido, paciente.correo, paciente.telefono, paciente.password]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ninguno de los campos puede ser nulo")
    # Validar el RUT
    if not validar_rut(paciente.rut):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="RUT inválido")
        # Validar el dominio del correo electrónico
    
    # Convertir el modelo a un diccionario
    paciente_dict = jsonable_encoder(paciente)
    logging.info(f"post paciente with: {paciente_dict}")
    paciente_dict = dict(paciente)
   

    # Buscar si el dato ya existe
    db_data = await db["paciente"].find_one({"rut": paciente.rut})
    if db_data:
        # Si el dato ya existe, retornar un error
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Data already exists")

    # Si el dato no existe, crearlo con sus fechas de creación
    paciente_dict['created_at'] = datetime.now()
    paciente_dict['updated_at'] = datetime.now()
    new_data = await db["paciente"].insert_one(paciente_dict)

    # Retornar el id del nuevo dato
    return str(new_data.inserted_id)


@router.get("/paciente")
async def get_paciente(rut: str = None, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))) -> List[Paciente] | Paciente:
    """Endpoint para obtener un dato de la base de datos"""
    # Buscar el dato por el nombre
    if rut is None:
        logging.info("get all pacientes")
        try:
            data = await db["paciente"].find().to_list(length=100)
            if data is None:
                data = []
        except Exception as err:
            logging.error(err)
        return data

    logging.info(f"get paciente with rut: {rut}")
    data = await db["paciente"].find_one({"rut": rut})

    if data:
        # Si el dato existe, retornarlo
        return data

    else:
        # Si el dato no existe, retornar un error
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, 
                            content={"message": "Data not found"})
    
@router.delete("/paciente/{rut}")
async def delete_paciente(rut: str, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="DELETE"))):
    """Endpoint para eliminar un paciente de la base de datos por RUT"""
    logging.info(f"Eliminando paciente con RUT: {rut}")

    # Verificar si existe el paciente con el RUT dado
    paciente = await db["paciente"].find_one({"rut": rut})
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    # Eliminar el paciente
    await db["paciente"].delete_one({"rut": rut})

    # Retornar un mensaje de éxito
    return {"message": f"Paciente con RUT: {rut} ha sido eliminado exitosamente."}

@router.put("/paciente/{rut}")
async def put_paciente_by_rut(rut: str, data: dict, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="PUT"))):
    """Endpoint para actualizar un paciente en la base de datos por RUT"""
    # Verificar si existe el paciente con el RUT dado
    paciente = await db["paciente"].find_one({"rut": rut})
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    # Actualizar solo los campos permitidos
    allowed_fields = {"nombre", "apellido", "correo"}
    updated_data = {key: value for key, value in data.items() if key in allowed_fields}

    # Verificar si se han proporcionado campos válidos para la actualización
    if not updated_data:
        raise HTTPException(status_code=400, detail="No se proporcionaron campos válidos para la actualización.")

    # Actualizar el dato
    updated_data['updated_at'] = datetime.now()

    # Realizar la actualización en la base de datos
    await db["paciente"].update_one({"rut": rut}, {"$set": updated_data})

    return {"message": f"Paciente con RUT: {rut} ha sido actualizado exitosamente."}

@router.get("/pacientes", response_model=List[Paciente])
async def get_pacientes(db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))):
    """Endpoint para obtener todos los pacientes de la base de datos"""
    # Buscar todos los pacientes
    logging.info("Obteniendo todos los pacientes")
    try:
        pacientes = await db["paciente"].find().to_list(length=100)
        if not pacientes:
            pacientes = []
    except Exception as err:
        logging.error(err)
        raise HTTPException(status_code=500, detail="Error interno del servidor")

    return pacientes

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


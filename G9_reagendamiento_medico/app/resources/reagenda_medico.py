import logging
from typing import List
from fastapi import APIRouter, status, Depends,HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.model import CalendarioR

from app.auth import get_db


from itertools import cycle

router = APIRouter(
    tags=["reagenda_medico"],
    responses={404: {"description": "Not found"}},
)


# Listamos todas las citas agendadas para el rut consultado
@router.get("/calendario_re/{rut}")
async def get_atenciones(rut: str,db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))) -> List[CalendarioR]:#| CalendarioR:
    """Endpoint para obtener el listado filtrado por especialidades de la colección Calendario"""
    if rut is None:
        try:
            calendarios = await db["calendario"].find({"rut": rut, "status": "confirmada"}).to_list(length=100)
            if calendarios is None: 
                calendarios = []
            return calendarios
            #return [CalendarioR(**calendario) for calendario in calendarios]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")
    data = await db["calendario"].find({"rut": rut}).to_list(length=100)
    if data: 
        return data
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content={"message":"Data not found"})

# Listamos la cita agendada la el rut y numero de atencion     
@router.get("/calendario_re/{rut}/{nro_atencion}")
async def get_atenciones_nro(rut: str, nro_atencion: int,db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))) -> List[CalendarioR]:#| CalendarioR:
    """Endpoint para obtener la cita medica que tiene agendado un paciente"""
    if rut is None or nro_atencion is None:
        try:
            calendarios = await db["calendario"].find({"rut": rut, "nro_atencion": nro_atencion, "status": "confirmada"}).to_list(length=100)
            if calendarios is None: 
                calendarios = []
            return calendarios
            #return [CalendarioR(**calendario) for calendario in calendarios]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")
    data = await db["calendario"].find({"rut": rut, "nro_atencion": nro_atencion}).to_list(length=100)
    if data: 
        return data
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content={"message":"Data not found"})
    

#Generamos el metodo para registrar en coleccion calendario_mod las citas canceladas y reagendadas

@router.post("/calendario_mod")
async def post_reagenda(rut: str, nro_atencion: int, estado: str, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="POST"))):
    """Endpoint actualiza la coleccion calendario y guarda el dato modificado en la coleccion calendario_mod"""

    # Validar campos no nulos
    if not all([rut, nro_atencion, estado]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ninguno de los campos puede ser nulo")
    
    # Buscar el calendario en la base de datos
    calendario_data = await db["calendario"].find_one({"rut": rut, "nro_atencion": nro_atencion})
    # Obtener todos los campos del calendario
    correo = calendario_data.get("correo", "")
    telefono = calendario_data.get("telefono", "")
    prevision = calendario_data.get("prevision", "")
    centro_medico = calendario_data.get("centro_medico", "")
    especialidad = calendario_data.get("especialidad", "")
    nombre_medico = calendario_data.get("nombre_medico", "")
    fecha = calendario_data.get("fecha", "")
    hora = calendario_data.get("hora", "")
    status = calendario_data.get("status", "")

    # calendario.status += "-" + estado
    status += "-" + estado

    # Convertir el modelo a un diccionario
    calendario_mod_dict = {
        "correo": correo,
        "telefono": telefono,
        "rut": rut,
        "prevision": prevision,
        "centro_medico": centro_medico,
        "especialidad": especialidad,
        "nombre_medico": nombre_medico,
        "fecha": fecha,
        "hora": hora,
        "status": status,
        "nro_atencion": nro_atencion,
        'created_at': datetime.now(),
        'updated_at': datetime.now()
    }
   
    # Buscar si el dato ya existe
    # Insertar el nuevo dato en calendario_mod
    new_data = await db["calendario_mod"].insert_one(calendario_mod_dict)

    # Llamar al método para actualizar el estado en la base de datos calendario
    await update_calendario_status(rut, nro_atencion, db)
    # Actualizar el estado en la colección calendario

    # Retornar el id del nuevo dato
    return str(new_data.inserted_id)

   
#metodo para actualiza calendario y dejarla cita disponible cuando se reagende o cancele una cita
async def update_calendario_status(rut: str, nro_atencion: int, db: AsyncIOMotorClient):
    try:
        await db["calendario"].update_one(
            {"rut": rut, "nro_atencion": nro_atencion},
            {"$set": {  "correo": "","telefono": "","rut": "", "prevision": "","status": "Disponible","nro_atencion": 0}},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating calendario status: {e}")

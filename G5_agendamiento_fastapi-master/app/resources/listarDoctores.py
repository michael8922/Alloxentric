import logging
from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from itertools import cycle
from app.models.model import Calendario, UpdateAppointmentModel


from app.auth import get_db
from app.models.model import ExampleModel

router = APIRouter(
    tags=["listarDoctores"],
    responses={404: {"description": "Not found"}},
)

@router.get("/validaRut/{rut}")
async def example1(rut: str):
    """Endpoint de valida rut"""

    logging.info("Example1")
    
    try:
        is_valid, formatted_rut = validate_rut(rut)
        if is_valid:
            return JSONResponse(content=[{"message": "ok", "name": "test", "rut": formatted_rut}])
        else:
            return JSONResponse(content=[{"message": "reject", "name": "test"}])
    except Exception as e:
        logging.error(f"Internal Server Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def validate_rut(rut):
    # Eliminar espacios en blanco del RUT ingresado
    rut = rut.replace(' ', '')

    # Eliminar guiones y puntos del RUT y contar caracteres
    rut_clean = rut.replace('-', '').replace('.', '')

    # Verificar si el RUT tiene la cantidad correcta de dígitos
    if len(rut_clean) < 8 or len(rut_clean) > 9 or not rut_clean[:-1].isdigit():
        return False, None

    # Separar el dígito verificador del resto del RUT
    rut_number = rut_clean[:-1]
    dv = rut_clean[-1]

    # Ajustar el RUT a un formato estándar XX.XXX.XXX-D
    if len(rut_clean) == 9:
        rut_formatted = f'{rut_number[:2]}.{rut_number[2:5]}.{rut_number[5:8]}-{dv}'
    else:
        rut_formatted = f'{rut_number[:1]}.{rut_number[1:4]}.{rut_number[4:7]}-{dv}'

    # Lógica de validación del RUT
    revertido = map(int, reversed(str(rut_number)))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(revertido, factors))
    res = (-s) % 11

    # Convertir el dígito verificador a mayúscula si es una letra
    if dv.isalpha():
        dv = dv.upper()

    # Verificar si el dígito verificador es correcto (mayúscula o minúscula 'K')
    if str(res) == dv:
        return True, rut_formatted
    else:
        return False, rut_formatted
    

@router.get("/calendario_filtros", response_model=List[Calendario])
async def get_calendario_filtered(
    db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))
) -> List[Calendario]:
    """Endpoint para obtener registros filtrados por especialidad, centro médico, nombre de médico y estado disponible"""
    try:
        calendarios = await db["calendario"].find({
            "especialidad": "MEDICINA GENERAL",
            "centro_medico": "Megasalud",
            "nombre_medico": "Juan Labra",
            "status": "disponible"
        }).to_list(length=100)

        if not calendarios:
            return []

        return [Calendario(**calendario) for calendario in calendarios]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")
    
@router.put("/update_appointment/{nro_orden}")
async def update_appointment(nro_orden: str, update_data: UpdateAppointmentModel, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="PUT"))):
    try:
        logging.info(f"Trying to update appointment with order number: {nro_orden}")
        appointment_collection = db["calendario"]

        # Verificar si la cita existe utilizando el número de orden
        appointment = await appointment_collection.find_one({"nro_orden": nro_orden})
        if appointment is None:
            logging.error("Appointment not found. Check if the order number matches an existing appointment.")
            raise HTTPException(status_code=404, detail="Cita no encontrada")

        # Convertir el modelo de actualización a un diccionario
        update_data_dict = update_data.dict(exclude_unset=True)

        # Obtener el estado actual de la cita
        current_status = appointment.get('status', '')

        # Verificar si el estado actual es "Disponible" para actualizar a "Reservada"
        if current_status == "disponible" and 'status' not in update_data_dict:
            update_data_dict['status'] = "reservada"

        # Actualizar los campos de la cita excepto nro_orden
        for field, value in update_data_dict.items():
            if field != 'nro_orden':
                appointment[field] = value

        # Actualizar la cita en la base de datos
        await appointment_collection.replace_one({"nro_orden": nro_orden}, appointment)

        return {"message": "Cita actualizada exitosamente"}
    
    except Exception as e:
        logging.error(f"Error al actualizar la cita: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno al actualizar la cita")
    


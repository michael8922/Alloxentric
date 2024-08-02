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
    tags=["anularCitas"],
    responses={404: {"description": "Not found"}},
)


@router.get("/calendario_filtros/{rut}", response_model=List[Calendario])
async def get_calendario_by_rut(
    rut: str,
    db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))
) -> List[Calendario]:
    """Endpoint para obtener registros filtrados por Rut."""
    try:
        calendarios = await db["calendario"].find({
            "rut": rut
        }).to_list(length=100)

        if not calendarios:
            return []

        return [Calendario(**calendario) for calendario in calendarios]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")
    

@router.put("/update_appointment/{nro_orden}")
async def update_appointment(
    nro_orden: str,
    update_data: UpdateAppointmentModel,
    db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="PUT"))
):
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

        # Establecer valores por defecto si los campos no están presentes en los datos de actualización
        default_values = {
            "correo": "",
            "telefono": "",
            "rut": "",
            "prevision": "",
            "nombre_paciente": "",
            "status": "disponible"
        }

        # Actualizar los campos con los valores predeterminados si no están presentes
        for field, default_value in default_values.items():
            if field not in update_data_dict:
                update_data_dict[field] = default_value

        # Actualizar la cita en la base de datos
        await appointment_collection.update_one(
            {"nro_orden": nro_orden},
            {"$set": update_data_dict}
        )

        return {"message": "Cita actualizada exitosamente"}
    
    except Exception as e:
        logging.error(f"Error al actualizar la cita: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno al actualizar la cita")
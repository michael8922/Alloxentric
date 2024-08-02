import logging
import random
from typing import List, Optional
from fastapi import APIRouter, Query, status, Depends,HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.model import ConfMedico, Calendario, CrearHora, UpdateAppointmentModel


from app.auth import get_db


from itertools import cycle


router = APIRouter()

router = APIRouter(
    tags=["conf_medicos"],
    responses={404: {"description": "Not found"}},
)



@router.post("/conf_medico")
async def post_medico(confmedico: ConfMedico, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="POST"))):
    """Endpoint para crear un dato en la base de datos del Medico"""

    # Validar campos no nulos
    if not all([confmedico.rut, confmedico.nombre, confmedico.apellido, confmedico.correo, confmedico.telefono, confmedico.correo, confmedico.direccion, confmedico.secret,confmedico.especialidad,confmedico.centro_medico]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ninguno de los campos puede ser nulo")
    
    # Convertir el modelo a un diccionario
    medico_dict = jsonable_encoder(confmedico)
    logging.info(f"post medico with: {medico_dict}")
    medico_dict = dict(confmedico)
   

    # Buscar si el dato ya existe
    db_data = await db["conf_medico"].find_one({"rut": confmedico.rut})
    if db_data:
        # Si el dato ya existe, retornar un error
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Data already exists")

    # Si el dato no existe, crearlo con sus fechas de creación
    medico_dict['created_at'] = datetime.now()
    medico_dict['updated_at'] = datetime.now()
    new_data = await db["conf_medico"].insert_one(medico_dict)

    # Retornar el id del nuevo dato
    return str(new_data.inserted_id)


@router.get("/conf_medico")
async def get_confmedico(rut: str = None, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))) -> List[ConfMedico]:
    #| ConfMedico:
    """Endpoint para obtener un dato de la base de datos"""
    # Buscar el dato por el nombre
    if rut is None:
        logging.info("get all medicos")
        try:
            data = await db["conf_medico"].find().to_list(length=100)
            if data is None:
                data = []
        except Exception as err:
            logging.error(err)
        return data

    logging.info(f"get medico with rut: {rut}")
    data = await db["conf_medico"].find_one({"rut": rut})

    if data:
        # Si el dato existe, retornarlo
        return data

    else:
        # Si el dato no existe, retornar un error
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, 
                            content={"message": "Data not found"})
    
@router.delete("/conf_medico/{rut}")
async def delete_medico(rut: str, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="DELETE"))):
    """Endpoint para eliminar un medico de la base de datos por RUT"""
    logging.info(f"Eliminando medico con RUT: {rut}")

    # Verificar si existe el Medico con el RUT dado
    medico = await db["conf_medico"].find_one({"rut": rut})
    if not medico:
        raise HTTPException(status_code=404, detail="Medico no encontrado")

    # Eliminar el medico
    await db["conf_medico"].delete_one({"rut": rut})

    # Retornar un mensaje de éxito
    return {"message": f"Medico con RUT: {rut} ha sido eliminado exitosamente."}

@router.put("/conf_medico/{rut}")
async def put_medico_by_rut(rut: str, data: dict, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="PUT"))):
    """Endpoint para actualizar un medico en la base de datos por RUT"""
    # Verificar si existe el medico con el RUT dado
    medico = await db["conf_medico"].find_one({"rut": rut})
    if not medico:
        raise HTTPException(status_code=404, detail="Medico no encontrado")

    # Actualizar solo los campos permitidos
    allowed_fields = {"nombre", "apellido", "correo","direccion","secret"}
    updated_data = {key: value for key, value in data.items() if key in allowed_fields}

    # Verificar si se han proporcionado campos válidos para la actualización
    if not updated_data:
        raise HTTPException(status_code=400, detail="No se proporcionaron campos válidos para la actualización.")

    # Actualizar el dato
    updated_data['updated_at'] = datetime.now()

    # Realizar la actualización en la base de datos
    await db["conf_medico"].update_one({"rut": rut}, {"$set": updated_data})

    return {"message": f"Medico con RUT: {rut} ha sido actualizado exitosamente."}

@router.get("/conf_medicos", response_model=List[ConfMedico])
async def get_medicos(db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))):
    """Endpoint para obtener todos los medicos de la base de datos"""
    # Buscar todos los medicos
    logging.info("Obteniendo todos los medicos")
    try:
        conf_medicos = await db["conf_medico"].find().to_list(length=100)
        if not conf_medicos:
            conf_medicos = []
    except Exception as err:
        logging.error(err)
        raise HTTPException(status_code=500, detail="Error interno del servidor")

    return conf_medicos

@router.get("/medico/{especialidad}", response_model=List[ConfMedico])
async def get_medicos_by_especialidad(especialidad: str, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))):
    """Endpoint para obtener médicos por especialidad"""
    # Buscar médicos por la especialidad proporcionada
    try:
        data = await db["calendario"].find({"especialidad": especialidad}).to_list(length=100)
        if not data:
            return []
    except Exception as err:
        logging.error(err)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": "Error interno del servidor"})

    return data

@router.get("/calendario/{especialidad}", response_model=List[Calendario])
async def get_calendario_by_especialidad(especialidad: str,db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))) -> List[Calendario]| Calendario:
    """Endpoint para obtener el listado filtrado por especialidades de la colección Calendario"""
    try:
        calendarios = await db["calendario"].find({"especialidad": especialidad, "status": "disponible"}).to_list(length=100)
        if not calendarios:
            return []
        return [Calendario(**calendario) for calendario in calendarios]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")


@router.get("/calendario/{especialidad}/{centro_medico}", response_model=List[Calendario])
async def get_calendario_by_especialidad_and_centro(especialidad: str,centro_medico: str,db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))) -> List[Calendario]:
    """Endpoint para obtener el listado filtrado por especialidad y centro médico de la colección Calendario"""
    try:
        calendarios = await db["calendario"].find({"especialidad": especialidad,"centro_medico": centro_medico, "status": "disponible"}).to_list(length=100)
        
        if not calendarios:
            return []
        
        return [Calendario(**calendario) for calendario in calendarios]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")

@router.get("/calendario/{especialidad}", response_model=List[Calendario])
async def get_calendario_by_especialidad_and_centro(especialidad: str,db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))) -> List[Calendario]:
    """Endpoint para obtener el listado filtrado por especialidad y centro médico de la colección Calendario"""
    try:
        calendarios = await db["calendario"].find({"especialidad": especialidad,"status": "disponible"}).to_list(length=100)
        
        if not calendarios:
            return []
        
        return [Calendario(**calendario) for calendario in calendarios]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")
    

@router.get("/calendario/{especialidad}/{centro_medico}/{fecha}", response_model=List[Calendario])
async def get_calendario_by_especialidad_centro_and_fecha(
    especialidad: str,
    centro_medico: str,
    fecha: str,  # La fecha se recibe como una cadena
    db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))
) -> List[Calendario]:
    """Endpoint para obtener el listado filtrado por especialidad, centro médico y fecha de la colección Calendario"""
    try:
        calendarios = await db["calendario"].find({
            "especialidad": especialidad,
            "centro_medico": centro_medico,
            "fecha": fecha,
            "status": "disponible"  # Filtrar calendarios con fecha igual o posterior a la proporcionada
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


# async def get_last_order(db: AsyncIOMotorClient):
#     """Función para obtener el último número de orden almacenado en la colección 'calendario'"""

#     # Realizar la búsqueda del último número de orden
#     last_order_doc = await db["calendario"].find_one(
#         sort=[("nro_orden", -1)],  # Ordenar por número de orden en orden descendente
#         projection={"nro_orden": True}  # Obtener solo el campo nro_orden
#     )

#     # Si no hay documentos con número de orden, se asigna el número 1
#     if not last_order_doc or 'nro_orden' not in last_order_doc:
#         return "1"

#     return last_order_doc['nro_orden']

async def get_last_order(nro_orden:str, db: AsyncIOMotorClient):
    """Función para obtener el último número de orden almacenado en la colección 'calendario'"""

    # Realizar la búsqueda del último número de orden
    last_order_doc = await db["calendario"].find_one({"nro_orden": nro_orden})

    # Si no hay documentos con número de orden, se asigna el número 1
    if not last_order_doc:
        return "0"
    return "1"

@router.post("/crear_hora")
async def crear_hora(crear_hora: CrearHora, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="POST"))):
    """Endpoint para crear una hora en la colección 'calendario'"""

    # Validar campos no nulos
    if not all([crear_hora.centro_medico, crear_hora.especialidad, crear_hora.nombre_medico, crear_hora.fecha, crear_hora.hora]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ninguno de los campos puede ser nulo")
    
    # Definir el estado como 'Disponible'
    status_value = "disponible"

    # Convertir el modelo a un diccionario
    hora_dict = crear_hora.dict()

    # Asignar el estado al diccionario antes que el número de orden
    hora_dict['status'] = status_value

    # Obtener el último número de orden
    # last_order = await get_last_order(db)

    # Incrementar el número de orden
    # next_order = str(int(last_order) + 2)
    fechaorder=crear_hora.fecha.replace('-','')
    next_order = fechaorder+str(random.randint(1, 1000))
    while True:
            last_order = await get_last_order(next_order,db)
            if last_order == "0":
                break
                #print("nada")
            else:
                print(f"Nro order existe :"+ next_order)
                next_order = fechaorder+str(random.randint(1, 1000))

    # Asignar el siguiente número de orden al diccionario
    hora_dict['nro_orden'] = next_order

    # Asignar fechas de creación
    hora_dict['created_at'] = datetime.now()
    hora_dict['updated_at'] = datetime.now()

    # Insertar la hora en la colección 'calendario'
    new_data = await db["calendario"].insert_one(hora_dict)

    # Retornar el id del nuevo dato
    return str(new_data.inserted_id)


@router.get("/conf_medico/{rut}")
async def get_confmedico(rut: str, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))) -> ConfMedico:
    try:
        data = await db["conf_medico"].find_one({"rut": rut})
        if data:
            return data
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/countStatus/{rut_medico}/{fecha_inicio}/{fecha_fin}")
async def count_calendario_by_rut(
    rut_medico: str,
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None,
    db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))
):
    filter_dict = {"rut_medico": rut_medico}
    
    if fecha_inicio and fecha_fin:
        # Convertir las fechas de cadena a objetos datetime para realizar comparaciones
        date_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        date_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
        
        # Convertir las fechas de nuevo a cadena en el formato de la base de datos
        fecha_inicio = date_inicio.strftime("%Y-%m-%d")
        fecha_fin = date_fin.strftime("%Y-%m-%d")

        filter_dict["fecha"] = {"$gte": fecha_inicio, "$lte": fecha_fin}

    # Realizar consultas en la base de datos utilizando el cliente db
    count_reservada = await db.calendario.count_documents({"status": "reservada", **filter_dict})
    count_confirmada = await db.calendario.count_documents({"status": "confirmada", **filter_dict})
    count_cancelada = await db.calendario.count_documents({"status": "cancelada", **filter_dict})
    count_disponible = await db.calendario.count_documents({"status": "disponible", **filter_dict})

    return {
        "reservada": count_reservada,
        "confirmada": count_confirmada,
        "cancelada": count_cancelada,
        "disponible": count_disponible,
    }

@router.get("/calendarioFiltroRut/{rut_medico}/{fecha_inicio}/{fecha_fin}", response_model=List[Calendario])
async def get_calendario_by_especialidad_and_centro(
    rut_medico: str,
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None,
    db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))
) -> List[Calendario]:
    """Endpoint para obtener el listado filtrado por especialidad, centro médico y rango de fechas de la colección Calendario"""
    try:
        if fecha_inicio:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        else:
            fecha_inicio_dt = datetime.now()

        if fecha_fin:
            fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
        else:
            fecha_fin_dt = fecha_inicio_dt + timedelta(days=7)  # Ejemplo: rango de una semana

        query = {
            "rut_medico": rut_medico,
            "fecha": {
                "$gte": fecha_inicio_dt.strftime('%Y-%m-%d'),
                "$lte": fecha_fin_dt.strftime('%Y-%m-%d')
            }
        }

        # Construir dinámicamente el filtro para campos no vacíos
        filtro_campos_no_vacios = {k: {"$ne": ""} for k in ["correo", "telefono", "rut", "prevision", "nombre_paciente"]}
        query.update(filtro_campos_no_vacios)

        calendarios = await db["calendario"].find(query).to_list(length=100)
        
        if not calendarios:
            return []
        
        return [Calendario(**calendario) for calendario in calendarios]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")


@router.get("/calendarioAgenda", response_model=List[Calendario])
async def get_calendario_by_fechas_and_rut_medico(
    rut_medico: str,
    fechas: List[str] = Query(..., alias="fecha"),  # Lista de fechas para filtrar
    db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))
) -> List[Calendario]:
    """Endpoint para obtener el listado filtrado por rut_medico y fechas de la colección Calendario"""
    try:
        # Consulta a la base de datos para buscar por rut_medico y fechas proporcionadas
        calendarios = await db["calendario"].find({
            "rut_medico": rut_medico,
            "fecha": {"$in": fechas}
        }).to_list(length=100)

        return [Calendario(**calendario) for calendario in calendarios]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")

@router.put("/update_cancelado/{nro_orden}")
async def update_appointment_status(nro_orden: str, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="PUT"))):
    try:
        logging.info(f"Trying to update status of appointment with order number: {nro_orden}")
        appointment_collection = db["calendario"]

        # Verificar si la cita existe utilizando el número de orden
        appointment = await appointment_collection.find_one({"nro_orden": nro_orden})
        if appointment is None:
            logging.error("Appointment not found. Check if the order number matches an existing appointment.")
            raise HTTPException(status_code=404, detail="Cita no encontrada")

        # Obtener el estado actual de la cita
        current_status = appointment.get('status', '')

        # Calcular el nuevo estado según el estado actual
        new_status = calculate_new_status(current_status)

        if new_status:
            # Actualizar solo el campo 'status'
            await appointment_collection.update_one({"nro_orden": nro_orden}, {"$set": {"status": new_status}})
            return {"message": f"Estado de la cita actualizado a {new_status} exitosamente"}

        raise HTTPException(status_code=400, detail="No se puede actualizar el estado de la cita")

    except Exception as e:
        logging.error(f"Error al actualizar el estado de la cita: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno al actualizar el estado de la cita")

def calculate_new_status(current_status):
    # Lógica para calcular el nuevo estado basado en el estado actual
    if current_status.lower() in ["disponible", "reservada", "confirmada"]:
        return "cancelada"
    return None

# @router.get("/calendarioFechasRut/{rut_medico}", response_model=List[Calendario])
# async def get_calendario_by_rut_medico(
#     rut_medico: str,
#     db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))
# ) -> List[Calendario]:
#     """Endpoint para obtener todos los registros de la colección 'calendario' filtrados por rut_medico."""
#     try:
#         calendarios = await db["calendario"].find({
#             "rut_medico": rut_medico
#         }).to_list(length=1000)  # Ajusta el límite según tus necesidades
        
#         if not calendarios:
#             return []

#         return [Calendario(**calendario) for calendario in calendarios]
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")
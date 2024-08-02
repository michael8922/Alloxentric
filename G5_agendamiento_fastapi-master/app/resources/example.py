import logging
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from itertools import cycle


from app.auth import get_db
from app.models.model import ExampleModel

router = APIRouter(
    tags=["example"],
    responses={404: {"description": "Not found"}},
)

@router.get("/example1")
async def example1():
    """Endpoint de ejemplo"""

    logging.info("Example1")
    # Retornar un mensaje de ejemplo
    return "Example1"

@router.get("/example1/{rut}")
async def example1(rut: str):
    """Endpoint de ejemplo"""

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

@router.post("/example2")
async def post_example2(data: ExampleModel, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="POST"))):
    """Endpoint para crear un dato en la base de datos"""
    # Convertir el modelo a un diccionario
    data = jsonable_encoder(data)
    logging.info(f"post example with: {data}")

    # Buscar si el dato ya existe
    db_data = await db["example"].find_one({"name": data['name']})
    if db_data:
        # Si el dato ya existe, retornar un error
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, 
                            content={"message": "Data already exists"})
    
    # Si el dato no existe, crearlo con sus fechas de creación
    data['created_at'] = datetime.now()
    data['updated_at'] = datetime.now()
    new_data = await db["example"].insert_one(data)

    # Retornar el id del nuevo dato
    return f"{new_data.inserted_id}"

@router.get("/example2")
async def get_example2(name: str = None, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))) -> List[ExampleModel] | ExampleModel:
    """Endpoint para obtener un dato de la base de datos"""
    # Buscar el dato por el nombre
    if name is None:
        logging.info("get all examples")
        try:
            data = await db["example"].find().to_list(length=100)
            if data is None:
                data = []
        except Exception as err:
            logging.error(err)
        return data

    logging.info(f"get example with name: {name}")
    data = await db["example"].find_one({"name": name})

    if data:
        # Si el dato existe, retornarlo
        return data

    else:
        # Si el dato no existe, retornar un error
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, 
                            content={"message": "Data not found"})

@router.put("/example2")
async def put_example2(data: ExampleModel, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="PUT"))):
    """Endpoint para actualizar un dato de la base de datos"""
    # Convertir el modelo a un diccionario
    data = jsonable_encoder(data)
    logging.info(f"put example with data: {data}")
    name = data["name"]
    data.pop("name")
    logging.info(f"put example with name: {name} and data: {data}")

    # Actualizar el dato
    data['updated_at'] = datetime.now()


    # Retornar un mensaje de éxito
    return "Ok"

@router.delete("/example2")
async def delete_example2(name: str, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="DELETE"))):
    """Endpoint para eliminar un dato de la base de datos"""
    logging.info(f"delete example with name: {name}")

    # Eliminar el dato
    await db["example"].delete_one({"name": name})

    # Retornar un mensaje de éxito
    return JSONResponse(status_code=status.HTTP_200_OK, 
                        content={"message": "Data deleted successfully"})

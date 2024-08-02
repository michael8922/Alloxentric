from bson import ObjectId
from typing import Optional
from pydantic import BaseModel


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class ExampleModel(BaseModel):
    name: str
    number: int
    # En la base de datos se guarda adicionalmente con fechas de creación y actualización

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

# class Paciente(BaseModel):
#     id: Optional[str] = None
#     rut: str
#     nombre: str
#     apellido: str
#     correo: str
#     telefono: str


class Medico(BaseModel):
    id: Optional[str] = None
    rut: str
    nombre: str
    apellido: str
    correo: str
    telefono: str
    especialidad: str
    prestacion: str
    centromedisco: str

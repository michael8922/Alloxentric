from bson import ObjectId
from typing import List
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

class Region(BaseModel):
    name_region: str


class Comuna (BaseModel):
    name_comuna: str
    region: Region

class CentroMedico (BaseModel):
    name_centro_medico: str

class Hora (BaseModel):
    hora : str

class Especialidad (BaseModel):
    especialidad: str

class Prevision(BaseModel):
    prevision: str

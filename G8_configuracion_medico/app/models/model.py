from bson import ObjectId
from typing import Optional
from pydantic import BaseModel
from typing import List

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


# class Medico(BaseModel):
#     id: Optional[str] = None
#     rut: str
#     nombre: str
#     apellido: str
#     correo: str
#     telefono: str
#     especialidad: str
#     prestacion: str
#     centromedisco: str


class ConfMedico(BaseModel):
    # id: Optional[str] = None
    rut: str
    nombre: str
    apellido: str
    correo: str
    telefono: str
    correo: str
    direccion: str
    secret: str
    especialidad: str
    centro_medico:List[str]
    confirm_wsp: bool
    confirm_mail: bool
    confirm_fono: bool
    list_wsp: bool
    list_mail: bool
    list_fono: bool


# class RutMedico(BaseModel):
#     rut: str
# class CanalMedicoConfirmacion(BaseModel):
#     # # id: Optional[str] = None
#     wsp: int
#     mail: int
#     fono: int
#     rut_medico: str

# class CanalMedicoListaeEpera(BaseModel):
#     # id: Optional[str] = None
#     wsp: int
#     mail: int
#     fono: int
#     rut_medico: str

class Calendario(BaseModel):
    correo: str
    telefono : str
    rut: str
    prevision: str
    centro_medico: str
    especialidad: str
    nombre_medico: str
    nombre_paciente: str
    fecha: str
    hora: str
    rut_medico: str
    status: str
    nro_orden: str

class UpdateAppointmentModel(BaseModel):
    correo: str
    telefono: str
    rut: str
    prevision: str 
    nombre_paciente: str 

class CrearHora(BaseModel):
    correo: str = ""
    telefono: str = ""
    rut: str = ""
    prevision: str = ""
    centro_medico: str
    especialidad: str
    nombre_medico: str
    nombre_paciente: str = ""
    fecha: str
    hora: str
    rut_medico: str
# def paciente_schema(paciente)-> dict:
#     return { "id": str(paciente["_id"]),
#              "rut": paciente["rut"],
#              "nombre": paciente["nombre"],
#              "apellido": paciente["apellido"],
#              "correo": paciente["correo"],
#              "telefono": paciente["telefono"]}


def medico(medico) -> dict:
    return {"id": str(medico["_id"]),
            "rut": medico["rut"],
            "nombre": medico["nombre"],
            "apellido": medico["apellido"],
            "correo": medico["correo"],
            "telefono": medico["telefono"],
            "especialidad": medico["especialidad"],
            "prestacion": medico["prestacion"],
            "centromedico": medico["centromedico"]            
            }

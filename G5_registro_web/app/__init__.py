def paciente_schema(paciente)-> dict:
    return { "id": str(paciente["_id"]),
             "rut": paciente["rut"],
             "nombre": paciente["nombre"],
             "apellido": paciente["apellido"],
             "correo": paciente["correo"],
             "telefono": paciente["telefono"]}
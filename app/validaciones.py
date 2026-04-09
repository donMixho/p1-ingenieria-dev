#validaciones para el microservicio de tareas

def validar_nombre_tarea(nombre):
    if not nombre:   #se utiliza el not para que el nombre no este vacio
        return {"error": "El nombre de la tarea no puede estar vacío"}
    if len(nombre) < 3:     #el len es para que cuente los caracteres del nombre
        return {"error": "El nombre debe tener al menos 3 caracteres"}
    if len(nombre) > 100:
        return {"error": "El nombre no puede superar los 100 caracteres"}
    return {"valido": True}  #validacion verdadera

def validar_id_tarea(id):
    if not isinstance(id, int):   #valida si el id no es un número entero
        return {"error": "El ID debe ser un número entero"}
    if id < 0:   #ayuda a validar que el id sea mayor que 0
        return {"error": "El ID debe ser mayor a 0"}
    return {"valido": True}
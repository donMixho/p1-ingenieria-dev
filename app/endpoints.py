# definimos una funcion para obtener tarea
def obtener_tarea_por_id(tareas, id):
    for tarea in tareas:
        if tarea["id"] == id:
            return tarea
    return {"error": "Tarea no encontrada"}


#definimos una funcion para eliminar tarea
def eliminar_tarea(tareas, id):
    for i, tarea in enumerate(tareas):
        if tarea["id"] == id:
            tareas.pop(i)
            return {"mensaje": "Tarea eliminada correctamente"}
    return {"error": "Tarea no encontrada"}


#definimos una funcion para identificar las tareas completadas 
def filtrar_tareas_completadas(tareas):
    return [t for t in tareas if t["completada"]]
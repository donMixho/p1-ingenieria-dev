# corregir error en la validación de tareas vacías

def corregir_lista_tareas(tareas):
    """
    Corrige el error donde una lista None causaba un crash.
    Se reemplaza None por una lista vacía.
    """
    #en caso que tareas este vacia retorna una lista vacia
    if tareas is None:
        return []
    return tareas  #si la lista tiene datos la valida y la devulve
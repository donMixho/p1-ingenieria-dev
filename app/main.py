#lo que esta en este codigo es como un ejemplo de algo que tener en los archivos al github
#Microservicio simple de gestión de tareas
tareas = []

def agregar_tarea(nombre):
    tarea = {"id": len(tareas) + 1, "nombre": nombre, "completada": False}
    tareas.append(tarea)
    return tarea

def listar_tareas():
    return tareas

def completar_tarea(id):
    for tarea in tareas:
        if tarea["id"] == id:
            tarea["completada"] = True
            return tarea
    return None

if __name__ == "__main__":
    agregar_tarea("Configurar repositorio Git")
    agregar_tarea("Crear pipeline DevOps")
    agregar_tarea("Documentar README")
    print("Tareas creadas:", listar_tareas())
    completar_tarea(1)
    print("Tarea 1 completada:", listar_tareas())
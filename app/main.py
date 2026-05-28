from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.validaciones import validar_nombre_tarea, validar_id_tarea
from app.endpoints import obtener_tarea_por_id, eliminar_tarea, filtrar_tareas_completadas

app = FastAPI(
    title="Microservicio Gestión de Tareas",
    description="API REST para gestionar tareas - Ingeniería DevOps EP2",
    version="2.0.0"
)

tareas = []

class TareaInput(BaseModel):
    nombre: str
    completada: Optional[bool] = False

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/tareas")
def listar_tareas():
    return tareas

@app.get("/tareas/completadas")
def listar_completadas():
    return filtrar_tareas_completadas(tareas)

@app.post("/tareas", status_code=201)
def agregar_tarea(tarea: TareaInput):
    val = validar_nombre_tarea(tarea.nombre)
    if "error" in val:
        raise HTTPException(status_code=400, detail=val["error"])
    nueva = {"id": len(tareas) + 1, "nombre": tarea.nombre, "completada": tarea.completada}
    tareas.append(nueva)
    return nueva

@app.get("/tareas/{id}")
def obtener_tarea(id: int):
    val = validar_id_tarea(id)
    if "error" in val:
        raise HTTPException(status_code=400, detail=val["error"])
    resultado = obtener_tarea_por_id(tareas, id)
    if "error" in resultado:
        raise HTTPException(status_code=404, detail=resultado["error"])
    return resultado

@app.put("/tareas/{id}/completar")
def completar_tarea(id: int):
    for tarea in tareas:
        if tarea["id"] == id:
            tarea["completada"] = True
            return tarea
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

@app.delete("/tareas/{id}")
def borrar_tarea(id: int):
    resultado = eliminar_tarea(tareas, id)
    if "error" in resultado:
        raise HTTPException(status_code=404, detail=resultado["error"])
    return resultado

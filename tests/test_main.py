import pytest
from fastapi.testclient import TestClient
from app.main import app, tareas

client = TestClient(app)

def setup_function():
    tareas.clear()

def test_health_check():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_crear_tarea():
    r = client.post("/tareas", json={"nombre": "Estudiar DevOps"})
    assert r.status_code == 201
    assert r.json()["nombre"] == "Estudiar DevOps"

def test_crear_tarea_nombre_vacio():
    r = client.post("/tareas", json={"nombre": ""})
    assert r.status_code == 400

def test_crear_tarea_nombre_muy_corto():
    r = client.post("/tareas", json={"nombre": "AB"})
    assert r.status_code == 400

def test_listar_tareas():
    client.post("/tareas", json={"nombre": "Tarea uno"})
    client.post("/tareas", json={"nombre": "Tarea dos"})
    r = client.get("/tareas")
    assert r.status_code == 200
    assert len(r.json()) == 2

def test_obtener_tarea_existente():
    post = client.post("/tareas", json={"nombre": "Tarea X"})
    id = post.json()["id"]
    r = client.get(f"/tareas/{id}")
    assert r.status_code == 200

def test_obtener_tarea_no_existente():
    r = client.get("/tareas/9999")
    assert r.status_code == 404

def test_completar_tarea():
    post = client.post("/tareas", json={"nombre": "Completar esta"})
    id = post.json()["id"]
    r = client.put(f"/tareas/{id}/completar")
    assert r.status_code == 200
    assert r.json()["completada"] == True

def test_eliminar_tarea():
    post = client.post("/tareas", json={"nombre": "Eliminar esta"})
    id = post.json()["id"]
    r = client.delete(f"/tareas/{id}")
    assert r.status_code == 200
    assert client.get(f"/tareas/{id}").status_code == 404

def test_listar_completadas():
    client.post("/tareas", json={"nombre": "Tarea pendiente"})
    post = client.post("/tareas", json={"nombre": "Tarea hecha"})
    id = post.json()["id"]
    client.put(f"/tareas/{id}/completar")
    r = client.get("/tareas/completadas")
    assert r.status_code == 200
    assert len(r.json()) == 1

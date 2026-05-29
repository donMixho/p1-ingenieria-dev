# p1-ingenieria-dev — Evaluación Parcial 2

**Nombre:** Leandro Rafael Ruiz Ruiz  
**Sección:** DOY0101 - 004D  
**Asignatura:** Ingeniería DevOps

---

## Descripción EP2

Microservicio REST de gestión de tareas en Python con FastAPI. Esta EP2 agrega un pipeline CI/CD completo sobre el repositorio de la EP1.

---

## Stack Tecnológico

| Componente | Tecnología |
|---|---|
| Lenguaje | Python 3.11 |
| Framework | FastAPI |
| Tests | pytest + pytest-cov |
| Contenedores | Docker (multi-stage) |
| Orquestación | Docker Compose |
| CI/CD | GitHub Actions |
| Seguridad | Snyk + Dependabot |

---

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/health` | Estado del servicio |
| GET | `/tareas` | Listar tareas |
| POST | `/tareas` | Crear tarea |
| GET | `/tareas/completadas` | Tareas completadas |
| GET | `/tareas/{id}` | Obtener tarea |
| PUT | `/tareas/{id}/completar` | Completar tarea |
| DELETE | `/tareas/{id}` | Eliminar tarea |

---

## Ejecutar localmente con Docker Compose

```bash
docker-compose up --build   # Levanta el servicio
# http://localhost:8000/docs  → documentación API
docker-compose down         # Detiene el servicio
```

---

## Ejecutar tests

```bash
pip install -r requirements.txt
pytest tests/ --cov=app -v
```

---

## Pipeline CI/CD

Se activa en cada push o PR a `main` o `develop`.
[1] Pruebas Automatizadas → pytest
[2] Análisis de Seguridad → Snyk (bloquea si hay vulnerabilidades críticas)
[3] Build Imagen Docker   → Dockerfile multi-stage
[4] Deploy Simulado       → Docker Compose (solo en main)

Cada job depende del anterior. Si tests o seguridad fallan, el deploy no ocurre. Todo queda trazado en la pestaña Actions de GitHub.

---

## Seguridad

- **Snyk:** Detecta CVEs en dependencias. Bloquea ante vulnerabilidades críticas.
- **Dependabot:** Abre PRs semanales con actualizaciones de dependencias.
- **Docker multi-stage:** Imagen de producción sin herramientas de desarrollo.
- **Usuario no-root:** Contenedor corre como `appuser`.

---

## Orquestación Docker Compose

- Límite CPU: 0.5 cores
- Límite memoria: 256 MB
- Health check cada 30 segundos
- Red interna `app-network`
- Reinicio automático `unless-stopped`

---
---

## Contenido EP1 ↓

# p1-ingenieria-dev

Repositorio para Evaluación Parcial 1 - Ingeniería Devops

Nombre: Leandro Rafael ruiz Ruiz

Seccion: DOY0101 - 004D

Microservicio de gestión de tareas desarrollado en Python.

---
## Estrategia de ramificación: GitFlow

Se eligió **GitFlow** este es un modelo de ramificación potente que puede ayudar a los equipos a gestionar proyectos de software complejos. Proporciona un flujo de trabajo estructurado, una estrategia de ramificación clara y una gestión eficaz de las versiones.

### Comparación de estrategias
Para este proyecto trabaje con dos ramas las cuales son GitFlow y Trunk-based development. Elegi GitFlow porque permite tener más orden en el desarrollo, ya que cada cambio pasa por varias ramas antes de llegar a main. Esto es útil cuando recién se está aprendiendo a trabajar con repositorios, porque queda un registro claro de qué se hizo y desde dónde. Trunk-based development es mas ágil pero requiere más experiencia con integración continua.

| Característica | GitFlow | Trunk-based |
|---|---|---|
| Ramas principales | main + develop | Solo main |
| Complejidad | Media | Baja |
| Ideal para | Proyectos con releases | Equipos con CI/CD avanzado |
| Control de versiones | Alto | Bajo |

### Ramas del proyecto
El repositorio está organizado en cuatro ramas, cada una con un rol distinto dentro del flujo de trabajo. Esta separación permite que el código en main siempre esté limpio y funcional, mientras que el desarrollo y las correcciones ocurren en ramas separadas sin afectar la versión estable.

| Rama | Propósito |
|---|---|
| `main` | Código estable en producción |
| `develop` | Integración de nuevas funcionalidades |
| `feature/agregar-endpoint` | Desarrollo de nueva funcionalidad |
| `hotfix/corregir-error` | Corrección urgente sobre main |

### Flujo de trabajo

1. Las nuevas funcionalidades se desarrollan en ramas `feature/` creadas desde `develop`
2. Al terminar, se hace un Pull Request de `feature/` hacia `develop`
3. Cuando `develop` está estable, se fusiona a `main` mediante Pull Request
4. Los errores urgentes se corrigen en ramas `hotfix/` creadas desde `main`

---

---

## Uso de los los commits durante el proceso

Para mantener el historial ordenado, los commits siguen el estándar Conventional Commits. La idea es que con solo leer el mensaje se entienda qué se hizo:

---

## Flujos de merge(unir, conbinar)

Dependiendo del tipo de cambio, el merge sigue un camino distinto dentro del repositorio:

| Flujo | Origen | Destino | Cuándo usarlo |
|---|---|---|---|
| Feature | `feature/<nombre>` | `develop` | Al terminar una nueva funcionalidad |
| Release | `develop` | `main` | Cuando develop está estable y listo |
| Hotfix | `hotfix/<nombre>` | `main` | Para correcciones urgentes en producción |

---

## Naming de ramas

Los nombres de las ramas siguen un formato fijo para que sea fácil identificar de qué se trata cada una:

| Tipo | Formato | Ejemplo |
|---|---|---|
| Feature | `feature/<descripcion>` | `feature/agregar-endpoint` |
| Hotfix | `hotfix/<descripcion>` | `hotfix/corregir-error` |
| Release | `release/<version>` | `release/v1.0.0` |

---

## Conclusion

Aprendi la importancia de tener una estructura clara de ramas en un repositorio. Ya que no entendia por qué habia que separar el main, develop y feature(se usa para evitar generar problemas entre los que trabajan en equipo aunque en este caso yo trabaje solo).
Me confundi varias veces entre las rutas de GitBash y GitHub, lo que me hiso cometer errores. Los resolvi gracias a la ayuda de compañeros, videos de youtube y comprendiendo conceptos con la ayuda de google e IA.
El uso o la aplicacion a lo que aprendi es por ejemplo si un un equipo de desarrollo real o de proyectos personales, GitFlow se usa para que varios programadores trabajen en paralelo sin chocar entre si.

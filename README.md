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

---

# Evaluación Parcial 3 - Observabilidad y Cumplimiento

Esta sección documenta las capacidades de observabilidad, orquestación y cumplimiento incorporadas al microservicio de gestión de tareas, junto con la trazabilidad del pipeline que garantiza la calidad del software antes de llegar a producción.

## 1. Observabilidad: Prometheus + Grafana

El microservicio expone métricas en tiempo real mediante la librería `prometheus-fastapi-instrumentator`, que publica un endpoint **`/metrics`** en el puerto 8000 con el formato estándar de Prometheus.

| Componente | Rol | Puerto |
|---|---|---|
| App FastAPI (`/metrics`) | Genera y expone las métricas | 8000 |
| Prometheus | Recolecta (scrape) las métricas cada 15s | 9090 |
| Grafana | Visualiza las métricas en dashboards | 3000 |

**Dashboard provisionado** (`monitoring/grafana/provisioning/dashboards/`): Grafana carga automáticamente un dashboard con cuatro paneles construidos sobre las métricas del instrumentator:

| Panel | Métrica base | Consulta PromQL |
|---|---|---|
| Requests por segundo (RPS) | `http_requests_total` | `sum(rate(http_requests_total[$__rate_interval]))` |
| Latencia p95 por endpoint | `http_request_duration_seconds_bucket` | `histogram_quantile(0.95, sum by (le, handler) (rate(...)))` |
| Tasa de errores (4xx / 5xx) | `http_requests_total{status=~"4.."/"5.."}` | `sum(rate(http_requests_total{status=~"5.."}[$__rate_interval]))` |
| Total de requests por endpoint | `http_requests_total` | `sum by (handler) (http_requests_total)` |

Toda la stack se levanta con `docker-compose up -d`, que orquesta la app, Prometheus y Grafana en la misma red.

## 2. Orquestación: Kubernetes (k3s) sobre EC2

El microservicio se despliega en un clúster **k3s** (Kubernetes ligero) ejecutándose sobre una instancia **EC2**. Los manifiestos viven en la carpeta `k8s/`:

| Recurso | Archivo | Descripción |
|---|---|---|
| Deployment | `k8s/deployment.yaml` | 1 réplica de la app, imagen `microservicio-tareas:latest` con `imagePullPolicy: Never` (imagen precargada en k3s) |
| Service | `k8s/service.yaml` | Tipo **NodePort**, expone el puerto 8000 de la app en el **nodePort 30080** |

**Características de resiliencia y control de recursos del Deployment:**

- **`readinessProbe`** a `/health`: evita enviar tráfico al pod hasta que la app esté lista.
- **`livenessProbe`** a `/health`: reinicia el pod automáticamente si deja de responder.
- **Límites de recursos:** `cpu 500m` / `memoria 256Mi`, con reservas (`requests`) de `250m` / `128Mi` para que el scheduler asigne el pod de forma predecible.

Acceso a la app una vez desplegada: `http://<IP-pública-EC2>:30080`.

## 3. Cumplimiento y calidad

El pipeline de CI/CD (`.github/workflows/ci-cd.yml`) incorpora controles automáticos que **bloquean** la entrega cuando no se cumplen los estándares:

| Control | Indicador | Comportamiento |
|---|---|---|
| **Quality gate de cobertura** | **IE6** | El job `quality-gate` lee la cobertura del `coverage.xml` y ejecuta `exit 1` si es **menor a 70%**, deteniendo el pipeline antes de `security`. |
| **Snyk (análisis de dependencias)** | — | El job `security` bloquea el pipeline ante CVE de severidad **crítica** (`--severity-threshold=critical`). |
| **Branch protection en `main`** | **IE5** | La rama `main` exige **Pull Request** obligatorio y **status checks** en verde antes de permitir el merge. |

Estos tres controles son acumulativos: un cambio solo llega a `main` si pasa las pruebas, alcanza la cobertura mínima, no introduce vulnerabilidades críticas y es revisado vía PR.

## 4. Trazabilidad: del commit a producción

El pipeline está encadenado mediante dependencias `needs:`, de modo que cada etapa actúa como **compuerta de calidad** de la siguiente. Si una falla, las posteriores no se ejecutan:

```
test  →  quality-gate  →  security  →  build  →  deploy
```

| Etapa | Qué garantiza | Decisión técnica que habilita |
|---|---|---|
| **test** | El código funciona: ejecuta la suite `pytest` y genera el reporte de cobertura. | Detectar regresiones antes de invertir en pasos costosos. |
| **quality-gate** | El código está suficientemente probado (cobertura ≥ 70%). | Rechazar código insuficientemente cubierto sin intervención manual. |
| **security** | No se introducen vulnerabilidades críticas conocidas. | Priorizar y remediar CVE según severidad reportada por Snyk. |
| **build** | La imagen Docker se construye reproduciblemente. | Validar que el artefacto desplegable es viable. |
| **deploy** | El servicio se despliega y responde en `/health`. | Confirmar disponibilidad real del servicio en el entorno destino. |

**Cómo las herramientas permiten tomar decisiones técnicas:**

- **Grafana/Prometheus** convierten el comportamiento del servicio en datos: si la latencia p95 sube o crece la tasa de errores 5xx, se puede decidir escalar réplicas, optimizar un endpoint o revertir un despliegue.
- **El quality gate y Snyk** transforman criterios subjetivos ("¿está bien probado?", "¿es seguro?") en umbrales objetivos y automáticos, eliminando la ambigüedad en la aprobación de cambios.
- **La trazabilidad del pipeline** deja un registro auditable de qué se validó y cuándo, de modo que cualquier fallo se ubica en la etapa exacta que lo detectó.

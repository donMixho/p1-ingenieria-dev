# p1-ingenieria-dev

Repositorio para Evaluación Parcial 1 - Ingeniería Devops

Nombre: Leandro Rafael ruiz Ruiz

Seccion: DOY0101 - 004D

Microservicio de gestión de tareas desarrollado en Python.

---
## Estrategia de ramificación: GitFlow

Se eligió **GitFlow** este es un modelo de ramificación potente que puede ayudar a los equipos a gestionar proyectos de software complejos. Proporciona un flujo de trabajo estructurado, una estrategia de ramificación clara y una gestión eficaz de las versiones.

### Comparación de estrategias

| Característica | GitFlow | Trunk-based |
|---|---|---|
| Ramas principales | main + develop | Solo main |
| Complejidad | Media | Baja |
| Ideal para | Proyectos con releases | Equipos con CI/CD avanzado |
| Control de versiones | Alto | Bajo |

### Ramas del proyecto

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

## Estructura del proyecto



## Uso de IA
Se utilizó Claude como apoyo para estructurar la documentación y guiar la configuración del
repositorio, ya que en un principio no contaba con conocimientos en ramas y en github, por
ende relice el paso a paso que se me mostro ya que no habia trabajado con gitflow.

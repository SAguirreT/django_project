# Laboratorio 06 — Motor de plantillas de Django

Este laboratorio refactoriza los templates del proyecto de farmacia para aplicar herencia, bloques, filtros, comentarios, includes y verificación de seguridad sin cambiar la lógica de las Views ni las URLs públicas.

## 1. Objetivo general

Se trabaja sobre la app `farmacia`, manteniendo su flujo actual:

`Navegador → URL existente → View → ORM → SQLite → Template refactorizado → respuesta`

La idea es mejorar la reutilización visual y la legibilidad del código sin alterar el comportamiento funcional ni mover ninguna pantalla a `/admin/`.

## 2. Qué significa la carpeta "antes"

La carpeta `antes` guarda una copia exacta del estado original de los templates que se fueron a modificar. Sirve para mostrar evidencia del código previo al refactor y comparar la versión original con la final.

En este laboratorio se guardan los archivos que fueron modificados antes de editar el proyecto real, con el nombre de archivo original. Eso permite documentar el cambio de forma clara en el informe y en la guía de evidencias.

### Ejemplo de uso

- `02_antes/templates/farmacia/entidad_list.html` = versión inicial
- `03_despues/templates/farmacia/entidad_list.html` = versión refactorizada

Esto hace visible el cambio entre:

- sin herencia ni bloques
- con `{% extends %}`, `{% block %}` y reutilización de código

## 3. Orden de la carpeta lab06

La carpeta principal del laboratorio tiene este orden lógico:

- `01_auditoria.md`  
  Documenta qué templates existen, qué usan `extends`, qué bloques tienen, si usan `include`, filtros y comentarios, y si hay riesgo de XSS.

- `02_antes/`  
  Contiene el estado original de los templates importantes antes del refactor. Aquí se guarda la evidencia “antes”.

- `03_despues/`  
  Contiene la versión ya refactorizada con herencia, filtros, comentarios y parciales reutilizables.

- `04_pruebas/`  
  Guarda la prueba automática del laboratorio (`test_templates.py`) para validar la seguridad, listados y flows de CRUD.

- `GUIA_EVIDENCIAS_LAB06.md`  
  Es la guía para tomar capturas y completar el Word/entrega con las evidencias del laboratorio.

- `README.md`  
  Explica el proceso completo para que el lector entienda la organización exacta del laboratorio.

## 4. Subcarpetas y su propósito

### `02_antes/templates/`
Es el respaldo de los templates originales. Se conserva el árbol similar al proyecto principal para entender qué se está modificando y evitar perder la base antes del refactor.

Se incluye esta estructura:

- `templates/base.html`
- `templates/farmacia/entidad_list.html`
- `templates/farmacia/entidad_confirm_delete.html`
- `templates/farmacia/venta_detail.html`
- `templates/farmacia/detalleventa_list.html`
- `templates/farmacia/detalleventa_confirm_delete.html`

### `03_despues/templates/`
Es la carpeta de resultados finales del laboratorio, donde ya aparecen los cambios aplicados:

- `base.html` con bloques básicos y footer
- listados con `{% extends %}`
- detalle de venta con contenido reutilizado
- confirmación de eliminación con `include`
- parciales en `templates/farmacia/partials/`

### `03_despues/templates/farmacia/partials/`
Aquí van los fragmentos reutilizables:

- `_confirm_delete.html` para las pantallas de eliminación
- `_venta_detalles.html` para la tabla del detalle de venta

Esto hace que no haya duplicación de código y que varias pantallas compartan la misma estructura.

### `04_pruebas/`
Incluye la prueba automatizada del laboratorio. Su objetivo es comprobar:

- que las URLs devuelven 200
- que el template base se usa correctamente
- que los valores de perfil vacío muestran `-`
- que la relación categoría-productos se lista bien
- que la venta y el detalle muestran decimales con dos cifras
- que el contenido HTML con `<script>` se escapa correctamente
- que las pantallas de confirmación usan el partial reutilizable

## 5. Qué se hizo en el laboratorio

### Fase 1 — Auditoría
Se revisaron los templates y se verificó:

- qué template hereda de `base.html`
- qué bloques usa
- qué filtros renderiza
- si tiene comentarios
- si existe duplicación o inclusión reutilizable
- si hay riesgo de XSS

### Fase 2 — Respaldo antes
Se copiaron los templates originales a `02_antes/` para tener evidencia del estado previo.

### Fase 3 — Base común
Se dejó la base del sitio con:

- `<!DOCTYPE html>`
- `block title`
- `meta charset` y `viewport`
- menú principal
- mensajes de Django
- bloque principal `content`
- pie de página

### Fase 4 — Herencia
Se migraron los templates importantes para que usen `{% extends 'base.html' %}` y el contenido quede dentro de `{% block content %}`.

### Fase 5 — Filtros, comentarios e include
Se aplicaron filtros como:

- `date:'d/m/Y'`
- `floatformat:2`
- `default:'-'`
- `length`
- `upper`

También se agregaron comentarios `{# ... #}` para explicar la relación 1:1, 1:N y N:M.

Y se reutilizó código con:

- `{% include 'farmacia/partials/_confirm_delete.html' %}`
- `{% include 'farmacia/partials/_venta_detalles.html' %}`

### Fase 6 — Pruebas automáticas
Se creó `test_templates.py` para validar que el refactor no rompió la funcionalidad y que el escape automático de Django sigue funcionando.

### Fase 7 — Seguridad
Se revisó que no haya:

- `|safe`
- `{% autoescape off %}`
- `mark_safe`

La validación con Django y el test de XSS confirma que Django escapa correctamente el HTML y evita inyección en plantillas.

## 6. Cómo leer esta carpeta correctamente

El orden correcto para estudiar el laboratorio es:

1. Leer `01_auditoria.md` para conocer el estado inicial.
2. Revisar `02_antes/` para ver la versión original.
3. Comparar con `03_despues/` para ver el resultado final.
4. Revisar `04_pruebas/` para ver la validación automática.
5. Usar `GUIA_EVIDENCIAS_LAB06.md` para preparar las capturas del Word.

## 7. Resultado esperado

Al final, la carpeta queda con evidencia clara de:

- qué se tenía antes
- qué se cambió
- cómo se validó
- qué quedó refactorizado y reutilizable

Eso hace que el laboratorio sea entendible, demostrable y fácil de defender en la entrega final.

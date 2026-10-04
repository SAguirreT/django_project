# Auditoría del Laboratorio 06

## 1) Inventario de templates y primera línea

| Archivo | Primera línea | Entidad | Tipo | extends | blocks | include | filtros | comentarios |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `templates/base.html` | `{% load static %}` | Base | base | — | `title`, `content` | — | — | `{# Bloques disponibles ... #}` |
| `templates/farmacia/inicio.html` | `{% extends 'base.html' %}` | Inicio | page | `base.html` | `content` | — | `{{ titulo }}` sin filtro | — |
| `templates/farmacia/comparacion.html` | `{% extends 'base.html' %}` | Comparación | list/detail | `base.html` | `content` | — | `{{ mejor_zona }}` sin filtro | — |
| `templates/farmacia/entidad_list.html` | `{% extends 'base.html' %}` | Genérico | list | `base.html` | `title`, `content` | — | `default`, `date`, `upper`, `length`, `floatformat` | `{# Este template sirve ... #}` |
| `templates/farmacia/entidad_form.html` | `{% extends 'base.html' %}` | Genérico | form | `base.html` | `title`, `content` | — | `singular|lower` | — |
| `templates/farmacia/entidad_confirm_delete.html` | `{% extends 'base.html' %}` | Genérico | delete | `base.html` | `title`, `content` | `_confirm_delete.html` | `singular|lower` | — |
| `templates/farmacia/zona_list.html` | `{% extends 'base.html' %}` | Zona | list | `base.html` | `content` | — | — | — |
| `templates/farmacia/zona_form.html` | `{% extends 'base.html' %}` | Zona | form | `base.html` | `content` | — | — | — |
| `templates/farmacia/farmacia_list.html` | `{% extends 'base.html' %}` | Farmacia | list | `base.html` | `content` | — | — | — |
| `templates/farmacia/farmacia_form.html` | `{% extends 'base.html' %}` | Farmacia | form | `base.html` | `content` | — | — | — |
| `templates/farmacia/evaluacion_list.html` | `{% extends 'base.html' %}` | Evaluación | list | `base.html` | `content` | — | — | — |
| `templates/farmacia/evaluacion_form.html` | `{% extends 'base.html' %}` | Evaluación | form | `base.html` | `content` | — | — | — |
| `templates/farmacia/evaluacion_detail.html` | `{% extends 'base.html' %}` | Evaluación | detail | `base.html` | `content` | — | — | — |
| `templates/farmacia/venta_detail.html` | `{% extends 'base.html' %}` | Venta | detail | `base.html` | `title`, `content` | `_venta_detalles.html` | `date`, `floatformat` | `{# Cada detalle ... #}` |
| `templates/farmacia/detalleventa_list.html` | `{% extends 'base.html' %}` | DetalleVenta | list | `base.html` | `title`, `content` | `_venta_detalles.html` | `floatformat` | — |
| `templates/farmacia/detalleventa_form.html` | `{% extends 'base.html' %}` | DetalleVenta | form | `base.html` | `content` | — | — | — |
| `templates/farmacia/detalleventa_confirm_delete.html` | `{% extends 'base.html' %}` | DetalleVenta | delete | `base.html` | `title`, `content` | `_confirm_delete.html` | — | — |
| `farmacia/templates/farmacia/inicio.html` | `{% extends 'base.html' %}` | Inicio (app dir) | page | `base.html` | `content` | — | — | — |
| `templates/farmacia/partials/_confirm_delete.html` | `<form method="post">` | Parcial | partial | — | — | — | — | — |
| `templates/farmacia/partials/_venta_detalles.html` | `<div class="table-wrap">` | Parcial | partial | — | — | — | `floatformat` | — |

## 2) Conteo de templates y herencia

- Total de templates bajo `templates/`: 18
- Templates que heredan directamente de `base.html`: 17
- `base.html` existe y define el encabezado, menú principal, footer y bloques `title` y `content`.
- No existe `base_form.html` en esta versión del proyecto.

## 3) Verificación de base.html

`base.html` sí existe en `farmacia_project/src/templates/base.html` y contiene:

- `<!DOCTYPE html>`
- `block title` con valor predeterminado `FarmaPoint`
- `meta charset` y `meta viewport`
- cabecera con marca `FarmaPoint`
- menú con enlaces a URLs reales (`inicio`, `entidad_list`, `detalleventa_list`, `zona_list`, etc.)
- bloque `content`
- pie de página
- bloque de mensajes Django (`if messages`)
- comentario de ayuda para plantillas hijas

## 4) Templates duplicados y orden de carga

La configuración del proyecto en `config/settings.py` tiene:

- `TEMPLATES['DIRS'] = [BASE_DIR / 'templates']`
- `APP_DIRS = True`

Esto significa que el directorio proyecto tiene prioridad sobre los templates de la app. Por eso los archivos de `templates/farmacia/` se cargan antes que `farmacia/templates/farmacia/` si hay un nombre repetido. En la práctica existe un homónimo:

- `src/templates/farmacia/inicio.html`
- `src/farmacia/templates/farmacia/inicio.html`

El proyecto usa el primero porque aparece en `DIRS` antes que `APP_DIRS`.

## 5) Resultado de `python manage.py check`

Salida verificada:

```bash
System check identified no issues (0 silenced).
```

## 6) Seguimiento de seguridad y XSS

No se encontraron coincidencias de `|safe`, `autoescape off` o `mark_safe` en los templates ni en las vistas del proyecto. Se verificó la salida real con los test de Django y se confirma que el escape automático de Django escapa cadenas HTML como `<script>`.

# Guía de evidencias — Laboratorio 06

## Preparación

```powershell
cd .\farmacia_project\src
python manage.py check
python manage.py test farmacia
python manage.py runserver
git status
git diff --stat
```

## PARTE 1 — Refactorizar los Templates de la aplicación Semana 4/5

### Ejercicio 1 — Auditar tus Templates actuales

**Qué se hizo:** Se revisó el árbol completo de templates y se confirmó que la app usa una estructura con `templates/` y `APP_DIRS` activo. La auditoría indica que los templates principales ya heredaban de `base.html` y que no había `|safe` ni `autoescape off`.

**Código antes / después:**

```django
# antes (lab06/antes/entidad_list.html)
{% extends 'base.html' %}
{% block title %}{{ plural }} | FarmaPoint{% endblock %}
```

```django
# después (farmacia_project/src/templates/farmacia/entidad_list.html)
{% extends 'base.html' %}
{# Este template sirve a varias entidades del CRUD y revisa la relación que corresponde en cada caso. #}
{% block title %}{{ plural }} | FarmaPoint{% endblock %}
```

**Capturas a tomar:**
- Abrir `farmacia_project/src/templates/farmacia/entidad_list.html` en VS Code.
- Abrir la URL `/clientes/` en el navegador.
- Ver que la cabecera y la tabla se muestran con la misma estructura.

**Resultado observado:** `<!-- Completar con lo observado en el navegador -->`

### Ejercicio 2 — Crear base.html

**Qué se hizo:** Se validó que `base.html` ya existía y se añadió el pie, mensajes Django y el comentario de bloques para las plantillas hijas, sin romper la navegación ni la base de estilos.

**Código antes / después:**

```django
# antes (lab06/antes/base.html)
<title>{% block title %}FarmaPoint{% endblock %}</title>
<main class="container content">{% block content %}{% endblock %}</main>
```

```django
# después (farmacia_project/src/templates/base.html)
{% if messages %}
    <ul class="messages">
        {% for message in messages %}
            <li class="{{ message.tags }}">{{ message }}</li>
        {% endfor %}
    </ul>
{% endif %}
<main class="container content">{% block content %}{% endblock %}</main>
<footer class="site-footer">...</footer>
{# Bloques disponibles para las plantillas hijas: title, content. #}
```

**Capturas a tomar:**
- Abrir `farmacia_project/src/templates/base.html`.
- Abrir la URL `/` y comprobar que el menú y el footer están presentes.

**Resultado observado:** `<!-- Completar con lo observado en el navegador -->`

### Ejercicio 3 — Migrar un Template existente a herencia

**Qué se hizo:** Se utilizó la plantilla genérica de listado y se reforzó su estructura con bloques y comentarios sin cambiar el flujo de vistas ni URLs.

**Código antes / después:**

```django
# antes (lab06/antes/entidad_list.html)
<div class="section-header"><h1>{{ plural }}</h1>...</div>
```

```django
# después (farmacia_project/src/templates/farmacia/entidad_list.html)
{% extends 'base.html' %}
{# Este template sirve a varias entidades del CRUD ... #}
<div class="section-header"><h1>{{ plural }}</h1>...</div>
```

**Capturas a tomar:**
- Abrir la URL `/categorias/`.
- Ver que el contenido de la tabla sigue igual y el layout se integra con `base.html`.

**Resultado observado:** `<!-- Completar con lo observado en el navegador -->`

### Ejercicio 4 — Migrar el resto de tus Templates

**Qué se hizo:** Se consolidó la estructura de la app para listas, formularios y confirmaciones sobre `base.html`, manteniendo los mismos nombres de rutas y contextos.

**Código antes / después:**

```django
# antes (lab06/antes/detalleventa_confirm_delete.html)
<form method="post">{% csrf_token %} ... </form>
```

```django
# después (farmacia_project/src/templates/farmacia/detalleventa_confirm_delete.html)
{% include 'farmacia/partials/_confirm_delete.html' with objeto=detalle volver='detalleventa_list' %}
```

**Capturas a tomar:**
- Abrir `farmacia_project/src/templates/farmacia/detalleventa_confirm_delete.html`.
- Abrir `/detalles-venta/<id>/eliminar/`.
- Ver el formulario con el mismo botón de confirmación y el enlace de cancelar.

**Resultado observado:** `<!-- Completar con lo observado en el navegador -->`

### Ejercicio 5 — Aplicar un filtro sobre un dato ya mostrado

**Qué se hizo:** Se aplicaron filtros sobre valores ya renderizados, como `default`, `date`, `floatformat` y `length` en listados y detalle de venta.

**Código antes / después:**

```django
# antes (lab06/antes/venta_detail.html)
<strong>Total registrado:</strong> S/ {{ venta.total }}
```

```django
# después (farmacia_project/src/templates/farmacia/venta_detail.html)
<p><strong>Total registrado:</strong> S/ {{ venta.total|floatformat:2 }}</p>
```

**Capturas a tomar:**
- Abrir `/ventas/1/`.
- Revisar el precio y subtotal con dos decimales en la tabla.

**Resultado observado:** `<!-- Completar con lo observado en el navegador -->`

### Ejercicio 6 — Documentar con comentarios

**Qué se hizo:** Se añadieron comentarios `{# ... #}` en el listado genérico y en la vista de detalle para explicar la relación 1:1, la 1:N inversa y la relación intermedia N:M.

**Código antes / después:**

```django
# antes
# sin comentarios descriptivos
```

```django
# después
{# Este template sirve a varias entidades del CRUD ... #}
{# Cada detalle representa la relación N:M ... #}
```

**Capturas a tomar:**
- Abrir el archivo `entidad_list.html` y `venta_detail.html` en VS Code.
- Confirmar que los comentarios están visibles en el código.

**Resultado observado:** `<!-- Completar con lo observado en el navegador -->`

### Ejercicio 7 — Reutilizar con include

**Qué se hizo:** Se creó el parcial `farmacia/partials/_confirm_delete.html` y se reutilizó en dos pantallas de eliminación; además se creó `_venta_detalles.html` para la tabla del modelo intermedio.

**Código antes / después:**

```django
# antes
<form method="post">{% csrf_token %} ... </form>
```

```django
# después
{% include 'farmacia/partials/_confirm_delete.html' with objeto=detalle volver='detalleventa_list' %}
```

**Capturas a tomar:**
- Abrir `farmacia_project/src/templates/farmacia/partials/_confirm_delete.html`.
- Abrir `/productos/1/eliminar/` y `/detalles-venta/1/eliminar/`.
- Ver que el mismo bloque se reutiliza.

**Resultado observado:** `<!-- Completar con lo observado en el navegador -->`

### Ejercicio 8 — Verificar seguridad y comparar con el Admin

**Qué se hizo:** Se verificó que no hay `|safe`, `autoescape off` ni `mark_safe` en los templates ni en las vistas. Se comprobó además que el escape automático de Django protege el contenido HTML.

**Procedimiento exacto:**
1. Crear un registro con `<script>alert('xss')</script>` en un campo de texto, por ejemplo nombre de producto o cliente temporal.
2. Abrir el listado correspondiente y pulsar `Ctrl + U`.
3. Buscar `&lt;script&gt;`.
4. Capturar la línea y eliminar el registro temporal al final.
5. Comparar con el flujo del Admin, donde la gestión interna y la autenticación de personal autorizado están separadas de la interfaz pública de usuario final.

**Capturas a tomar:**
- Abrir el listado con el campo de prueba en HTML renderizado.
- Código fuente con `Ctrl + U`.
- Buscar `&lt;script&gt;`.
- Captura del nombre del producto temporal.

**Resultado observado:** `<!-- Completar con lo observado en el navegador -->`

## PARTE 2 — Refactorizar los Templates de la investigación propia

### Ejercicio 9 — Auditar los Templates de tu investigación propia

**Qué se hizo:** El proyecto ya tenía las pantallas de categorías, clientes, ventas y detalle de venta listas para ser revisadas con foco en la relación 1:1 y 1:N inversa.

**Capturas a tomar:**
- Abrir `/categorias/` y `/clientes/` en el navegador.
- Revisar las relaciones mostradas por `producto.categoria`, `objeto.productos.all` y `objeto.perfil.direccion`.

**Resultado observado:** `<!-- Completar con lo observado en el navegador -->`

### Checklist antes de continuar — Parte 2

| Criterio | Estado |
| --- | --- |
| Existe `base.html` con menús y pie | Sí |
| `entidad_list.html` usa herencia | Sí |
| Hay comentarios explicativos | Sí |
| Hay filtros aplicados | Sí |
| Hay reutilización con `include` | Sí |
| Hay dos confirmaciones con partial | Sí |
| El CRUD sigue funcionando | Sí |
| No hay `|safe` ni `autoescape off` | Sí |
| Las URL no se movieron a `/admin/` | Sí |

### Ejercicio 10 — Migrar el resto de tus Templates

**Qué se hizo:** Se completó la estructura de las pantallas que muestran listas de entidades y detalle de venta para que reutilicen siempre el mismo layout base.

**Capturas a tomar:**
- Abrir `/ventas/1/`.
- Ver que se mantiene el mismo producto y la misma sección de total.

**Resultado observado:** `<!-- Completar con lo observado en el navegador -->`

### Ejercicio 11 — Reutilizar con include en la investigación propia

**Qué se hizo:** La tabla de detalle de venta se reutiliza con `_venta_detalles.html` y la confirmación de eliminación se centraliza con `_confirm_delete.html`.

**Capturas a tomar:**
- Abrir `farmacia_project/src/templates/farmacia/partials/_venta_detalles.html`.
- Abrir `/detalles-venta/`.
- Ver la misma estructura de tabla en todas las pantallas relevantes.

**Resultado observado:** `<!-- Completar con lo observado en el navegador -->`

### Ejercicio 12 — Verificar seguridad en un formulario existente

**Qué se hizo:** Se comprobó el flujo de escape y el render sin desactivar la protección automática. El contenido de texto se mantiene escapado en el HTML final.

**Procedimiento exacto:**
- Crear un producto o cliente con `<script>alert('xss')</script>`.
- Abrir la URL del listado.
- Ver el origen con `Ctrl + U` y buscar `&lt;script&gt;`.
- Eliminar el registro temporal al final.

**Capturas a tomar:**
- Captura del HTML renderizado del listado con la cadena escapada.
- Captura del código fuente con la cadena `&lt;script&gt;` visible.

**Resultado observado:** `<!-- Completar con lo observado en el navegador -->`

### Ejercicio 13 — Verificar el flujo completo (CRUD antes/después + comparación con el Admin)

**Qué se hizo:** Se revisó el flujo completo de creación, lectura, edición y eliminación sobre las pantallas refactorizadas, y se comparó con la gestión del Admin.

**Capturas a tomar:**
- Crear un cliente: `/clientes/` → botón Nuevo cliente.
- Listar con relaciones: `/clientes/`.
- Editar un cliente: `/cliente/<id>/editar/`.
- Eliminar: `/cliente/<id>/eliminar/`.
- Lista posterior a la eliminación.
- Repetir para una venta o detalle de venta con URL visible en la barra de direcciones (`/ventas/<id>/`, `/detalles-venta/`).

**Resultado observado:** `<!-- Completar con lo observado en el navegador -->`

> Borrador de comparación: El Admin resuelve la gestión interna para personal autorizado; las Views y templates propios permiten presentar relaciones y flujos orientados al usuario final de la farmacia, con identidad visual coherente, y siguen escapando automáticamente los datos.

### Ejercicio 14 — Publicar en GitHub

**Qué se hizo:** Se deja listo el contenido del laboratorio, la guía de evidencias y los backups de los templates para su revisión. No se hizo commit ni push.

**URL del repositorio:** `<!-- Pegar la URL real del repositorio -->`

**Mensaje sugerido de commit:**

```bash
git add farmacia_project/src/templates/base.html
git add farmacia_project/src/templates/farmacia/entidad_list.html
git add farmacia_project/src/templates/farmacia/entidad_confirm_delete.html
git add farmacia_project/src/templates/farmacia/venta_detail.html
git add farmacia_project/src/templates/farmacia/detalleventa_list.html
git add farmacia_project/src/templates/farmacia/detalleventa_confirm_delete.html
git add farmacia_project/src/templates/farmacia/partials/_confirm_delete.html
git add farmacia_project/src/templates/farmacia/partials/_venta_detalles.html
git add farmacia_project/src/farmacia/test_templates.py
git add lab06/01_auditoria.md
git add lab06/GUIA_EVIDENCIAS_LAB06.md
```

## Entregables

- `lab06/01_auditoria.md`
- `lab06/GUIA_EVIDENCIAS_LAB06.md`
- `lab06/antes/` con los backups originales
- `farmacia_project/src/templates/base.html`
- `farmacia_project/src/templates/farmacia/partials/_confirm_delete.html`
- `farmacia_project/src/templates/farmacia/partials/_venta_detalles.html`
- `farmacia_project/src/farmacia/test_templates.py`

## Conclusiones

- Se aplicó herencia con `base.html` y bloques de contenido para mantener una UI cohesiva.
- Se añadieron filtros y comentarios para mejorar legibilidad y presentación de las relaciones del dominio.
- Se reutilizaron parches visuales y formularios con `include` para evitar duplicación.
- Se verificó la seguridad del escape automático y se validó con pruebas de Django.

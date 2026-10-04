# FarmaPoint

Sistema web para la gestión de una farmacia. Permite administrar categorías, productos, proveedores, clientes y ventas de forma persistente.

## Problemática

El registro manual de productos, existencias, proveedores, clientes y ventas dificulta la consulta y actualización de información. FarmaPoint centraliza estos datos en una aplicación web con una base de datos SQLite.

## Tecnologías

- Python y Django
- SQLite
- Django ORM
- HTML y CSS

## Modelo de datos

El sistema conserva sus cinco entidades principales: `Categoria`, `Producto`,
`Proveedor`, `Cliente` y `Venta`. Se amplía con `PerfilCliente` y
`DetalleVenta`.

- `Categoria (1) ── (N) Producto`: una categoría puede agrupar productos.
- `Cliente (1) ── (N) Venta`: un cliente puede registrar varias ventas.
- `Cliente (1) ── (1) PerfilCliente`: la ficha complementaria tiene sentido
  únicamente para su cliente, por ello usa `on_delete=CASCADE`.
- `Venta (N) ── (M) Producto`, mediante `DetalleVenta`: el modelo intermedio
  conserva `cantidad` y `precio_unitario` para cada producto vendido.

Las vistas usan `select_related()` para relaciones 1:1 y claves foráneas, y
`prefetch_related('detalles__producto')` para recorrer eficientemente los
productos de una venta.

## Ejecución

Desde `farmacia_project/src`:

```bash
python manage.py migrate
python manage.py runserver
```

Abre `http://127.0.0.1:8000/`.

## CRUD de productos

- Crear: `/productos/nuevo/` → `ProductoForm.save()` → ORM → INSERT en SQLite.
- Consultar: `/productos/` → `Producto.objects.all()` → ORM → SELECT.
- Actualizar: `/productos/<id>/editar/` → `form.save()` → ORM → UPDATE.
- Eliminar: `/productos/<id>/eliminar/` → confirmación y POST → `delete()` → ORM → DELETE.

## CRUD de detalle de venta

- Crear y listar: `/detalles-venta/` y `/detalles-venta/nuevo/`.
- Editar: `/detalles-venta/<id>/editar/`.
- Eliminar: `/detalles-venta/<id>/eliminar/`, con confirmación y POST.

El detalle se inserta, actualiza o elimina con Django ORM; conceptualmente son
operaciones `INSERT`, `UPDATE` y `DELETE` sobre la tabla intermedia. La vista
`/ventas/<id>/` muestra el recorrido completo: URL → vista → ORM → SQLite →
contexto → template, incluyendo cada `DetalleVenta` y su `Producto`.

## Laboratorio 05 — Administrador de Django

El administrador está disponible en `/admin/`. Usa los mismos modelos y la misma
base SQLite que la interfaz de FarmaPoint. No se agregan modelos ni relaciones.

Se registran explícitamente las siete entidades con `admin.site.register(Modelo,
ModeloAdmin)`. Zona, Farmacia y EvaluacionUbicacion conservan su registro simple.

| Modelo | Columnas (`list_display`) | Búsqueda (`search_fields`) | Filtros (`list_filter`) | Edición relacionada |
| --- | --- | --- | --- | --- |
| Categoria | nombre, descripcion | nombre | — | — |
| Producto | nombre, categoria, precio, stock | nombre, descripcion | categoria | Selector de categoría (1:N) |
| Proveedor | nombre, telefono, correo | nombre, correo | — | — |
| Cliente | nombre, documento, telefono, correo | nombre, documento | — | PerfilCliente con StackedInline (1:1) |
| PerfilCliente | cliente, direccion, fecha_registro | nombre y documento del cliente | fecha_registro | — |
| Venta | id, cliente, fecha, total | nombre y documento del cliente | fecha | DetalleVenta con TabularInline (N:M) |
| DetalleVenta | venta, producto, cantidad, precio_unitario, subtotal | producto y nombre del cliente | — | — |

El perfil se edita dentro de Cliente. Su fecha de registro la genera el modelo.
Los detalles se editan dentro de Venta, con producto, cantidad y precio unitario
como columnas editables. `subtotal` es calculado por el modelo. El campo `total`
de Venta conserva el comportamiento existente: se introduce manualmente; editar
detalles no recalcula el total ni descuenta existencias automáticamente.

Desde `farmacia_project/src`, con el entorno virtual activado:

```powershell
python -m pip install -r requirements.txt
python manage.py check
python manage.py test farmacia
python manage.py runserver
```

Si aún no hay cuenta administradora, ejecutar `python manage.py createsuperuser`.
No es necesario crear otra si ya se puede iniciar sesión.

Las cinco pruebas nuevas de `farmacia/test_admin.py` comprueban búsqueda, filtros,
columnas, autenticación y creación, modificación y eliminación de las relaciones
1:1, 1:N y N:M a través de las vistas del Admin. Usan una base de pruebas separada
de los datos reales y complementan las tres pruebas previas.

El Admin resuelve la gestión interna de registros, permisos y formularios para
personal autorizado. Las vistas y plantillas de FarmaPoint siguen siendo
necesarias para la navegación, presentación y flujos del usuario final. El flujo
de administración es: usuario autorizado → URL /admin/ → ModelAdmin → ORM →
SQLite → plantilla del Admin → respuesta.

Las capturas requeridas y su secuencia se describen en `LAB05_EVIDENCIAS.md`.

## Laboratorio 06 — Motor de plantillas

Se refactorizaron las pantallas de lista y detalle de la app de farmacia para reutilizar una estructura base y mantener el mismo flujo URL → View → ORM → SQLite → Template.

### Templates involucrados

- `farmacia_project/src/templates/base.html` con cabecera, menú, mensajes y pie.
- `farmacia_project/src/templates/farmacia/entidad_list.html` para listados genéricos de `Categoria`, `Producto`, `Cliente`, `Venta` y `PerfilCliente`.
- `farmacia_project/src/templates/farmacia/venta_detail.html` para la vista detalle de una venta con productos.
- `farmacia_project/src/templates/farmacia/entidad_confirm_delete.html` y `detalleventa_confirm_delete.html` para confirmación de eliminación.

### Estructura de herencia

- `base.html` → plantillas de página directas (`entidad_list.html`, `venta_detail.html`)
- formularios adaptados con `extends 'base.html'` sin cambiar URLs ni lógica de vistas
- parcial reutilizable para confirmación y tabla del detalle de venta

### Filtros aplicados

| Template | Campo | Filtro |
| --- | --- | --- |
| `entidad_list.html` | `objeto.perfil.direccion` | `default:"-"` |
| `entidad_list.html` | `objeto.fecha_registro` | `date:"d/m/Y"` |
| `entidad_list.html` | `objeto.precio` | `floatformat:2` |
| `entidad_list.html` | `objeto.productos.all` | `length` |
| `venta_detail.html` | `venta.total` | `floatformat:2` |
| `venta_detail.html` | `detalle.precio_unitario` | `floatformat:2` |

### Parciales `include`

- `templates/farmacia/partials/_confirm_delete.html`: usado en las pantallas de confirmación de eliminación.
- `templates/farmacia/partials/_venta_detalles.html`: reutilizado en `venta_detail.html` y `detalleventa_list.html`.

### Verificación del auto-escape

Se comprobó que el contenido HTML es escapado automáticamente por Django, y no se usa `|safe` ni `{% autoescape off %}`. La prueba de XSS comprobó que `<script>` sale renderizado como `&lt;script&gt;` en el HTML final.

### Comandos para probar

```powershell
cd .\farmacia_project\src
python manage.py check
python manage.py test farmacia
python manage.py runserver
```

Luego abrir en el navegador:

- `http://127.0.0.1:8000/clientes/`
- `http://127.0.0.1:8000/categorias/`
- `http://127.0.0.1:8000/ventas/1/`
- `http://127.0.0.1:8000/detalles-venta/`

### Evidencias

La guía completa del laboratorio y el respaldo del estado original se encuentran en `lab06/GUIA_EVIDENCIAS_LAB06.md` y `docs/lab06/01_auditoria.md`.

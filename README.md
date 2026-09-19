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

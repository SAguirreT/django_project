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

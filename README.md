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

`Categoria (1) ── (N) Producto`  
`Cliente (1) ── (N) Venta`

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

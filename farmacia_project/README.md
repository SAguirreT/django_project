# FarmaPoint

FarmaPoint es una aplicación Django para administrar una farmacia y evaluar ubicaciones potenciales para nuevas boticas. El proyecto actual usa modelos ORM y SQLite; las notas de etapas anteriores que describían datos en memoria ya no aplican.

## Aplicación actual

El código Django está en `src/`, principalmente en la app `farmacia`.

- Modelos: `Categoria`, `Producto`, `Proveedor`, `Cliente`, `PerfilCliente`, `Venta`, `DetalleVenta`, `Zona`, `Farmacia` y `EvaluacionUbicacion`.
- Relaciones: Categoria 1:N Producto; Cliente 1:1 PerfilCliente; Cliente 1:N Venta; Venta N:M Producto mediante DetalleVenta; Zona 1:N Farmacia y EvaluacionUbicacion.
- Se conservan las vistas HTML, templates, formularios y Django Admin.
- Las consultas de vistas usan carga relacionada cuando corresponde.

## Ejecución

Desde `src/`, con el entorno virtual activo:

```powershell
python -m pip install -r requirements.txt
python manage.py check
python manage.py runserver
```

La web está en `http://127.0.0.1:8000/` y el Admin en `/admin/`.

## Laboratorio 08 — Django REST Framework

DRF está registrado en `config/settings.py`. La API utiliza los mismos modelos de `farmacia` y vive bajo `/api/v1/`:

- `/api/v1/productos/`: CRUD, búsqueda, orden, filtro de disponibilidad y acción `con-stock/`.
- `/api/v1/categorias/`: CRUD de categorías.
- `/api/v1/farmacias/`: CRUD, búsqueda, orden y filtro por `estado`.
- `/api/v1/ventas/`: lectura con cliente, detalles y productos anidados.
- `/api/v1/basico/productos/`: ejemplo con vistas genéricas para colección y detalle.

No se encontró el QuerySet personalizado de Semana 7 en el estado inicial. Para el filtro de disponibilidad se incorporó `ProductoQuerySet.con_stock()`, basado en el campo real `Producto.stock`; la guía lo identifica como adaptación.

La guía por ejercicio, comandos de prueba y lista de capturas con sus códigos/nombres están en [`LAB08_EVIDENCIAS.md`](LAB08_EVIDENCIAS.md). Para verificaciones automáticas:

```powershell
python manage.py test farmacia
python manage.py makemigrations --check --dry-run
```

No se realizaron commits ni push.

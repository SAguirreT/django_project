## Laboratorio 08 — Django REST Framework

Actualización del 17 de octubre de 2026. Integrantes: Dario Maza, Sheila Aguirre y Jose Contreras.

La aplicación ejecutable está en `farmacia_project/src`. Conserva las páginas HTML y `/admin/` y añade la API versionada `/api/v1/`.

| Recurso | Ruta | Operaciones |
|---|---|---|
| Categorías | `/api/v1/categorias/` | CRUD |
| Productos | `/api/v1/productos/` | CRUD; precio mayor que cero |
| Zonas | `/api/v1/zonas/` | CRUD |
| Farmacias | `/api/v1/farmacias/` | CRUD; distancia mayor que cero |
| Ventas | `/api/v1/ventas/` | Lectura; cliente, detalles y productos anidados |
| Evaluaciones | `/api/v1/evaluaciones/` | Lectura; zona anidada |

Los detalles usan `<id>/`. Las vistas genéricas del ejercicio 4 se conservan bajo `/api/v1/basico/productos/`, sin duplicar las rutas del router principal. Se mantiene `/api/v1/` del repositorio actual en lugar del `/api/` orientativo del PDF.

### Filtros y acciones

- Productos: `?search=Analgesico`, `?ordering=precio`, `?disponible=true` y acción `con-stock/`.
- Farmacias: `?search=Botica`, `?ordering=distancia_metros`, `?estado=Activa` y acción `activas/`.
- Los parámetros pueden combinarse con `&`. Las acciones reutilizan `ProductoQuerySet.con_stock()` y `FarmaciaQuerySet.activas()` y conservan filtros/paginación.
- Ventas: `select_related('cliente')` y `prefetch_related('detalles__producto__categoria')`.
- Evaluaciones: `select_related('zona')`.

### Instalación y comprobación

```powershell
cd farmacia_project/src
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py check
python manage.py test farmacia
python manage.py runserver
```

Se usan Django 5.2.17 y DRF 3.18.3. Las pruebas verifican CRUD, validación, filtros, relaciones anidadas, métodos 405 y consultas. Las mediciones serializan los mismos registros completos en ambas variantes.

### Datos ficticios y evidencias

```powershell
# Desde farmacia_project/src; la variable es opcional.
$env:FARMAPOINT_DB = Join-Path (Get-Location) 'lab08_demo.sqlite3'
python manage.py migrate
python manage.py sembrar_lab08
python manage.py runserver 127.0.0.1:8008
```

El cargador identifica todos los datos con LAB08 y conserva registros existentes. Sus ventas son datos de muestra, sin descontar existencias. El informe y los resultados reproducibles están en `lab08/` en la raíz del repositorio. La base SQLite no se publica.

La API usa los permisos predeterminados de DRF (AllowAny): en este laboratorio las escrituras son públicas. No constituye un despliegue protegido para producción. Ventas y evaluaciones solo admiten lectura por sus ViewSets. Los JSON y las capturas contienen únicamente los datos ficticios de la base de demostración.

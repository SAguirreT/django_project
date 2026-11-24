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


## Laboratorio 09 — React y Vite

Integrantes: Dario Maza, Sheila Aguirre y Jose Contreras.

Interfaz local con productos, categorías, búsqueda, stock y ventas con detalles anidados. Datos escritos a mano con la estructura JSON del Lab 08; todavía no consume la API.

```powershell
cd frontend
npm install
npm run dev
# Abrir http://localhost:5173/
npm run lint
npm run build
```

Consulta [las instrucciones del frontend](frontend/README.md) y [el informe del Lab 09](lab09/Informe_Lab09_FarmaPoint.pdf). `node_modules/` y `dist/` están excluidos de Git.

## Laboratorio 10 — Componentes, estado y eventos

Se reorganizó la interfaz original de Semana 9 conservando los datos y las reglas de la API de Semana 8. Las dos partes usan FarmaPoint, conforme a la investigación identificada en `frontend/README.md` desde el laboratorio anterior. Cada parte mantiene su propio catálogo y formulario; los datos son locales y se reinician al recargar. No se consume la API ni se pasan callbacks entre componentes.

### Ejecutar

```bash
cd frontend
npm install
npm run dev
```

Node.js 22.12 o superior (se verificó con Node 24). Validación: `npm run lint` y `npm run build`.

### Componentes en frontend/src/components

| Componente | Responsabilidad |
| --- | --- |
| ProductoCard | Props desestructuradas, stock predeterminado, contador local y botón de reserva limitado al stock. |
| ListaProductos | Catálogo en estado, búsqueda sin distinguir mayúsculas, filtro por categoría y formulario controlado; valida precio positivo, precisión, nombre y stock. |
| Tarjeta | Contenedor con título y children. |
| VentaCard | Relación Venta 1:N DetalleVenta y total calculado en céntimos. |
| DetalleItem | Producto anidado, cantidad y subtotal; adapta precio_unitario a precioUnitario. |
| Investigacion | Segunda instancia de la lista y relación M:N mediante DetalleVenta. |

Los datos originales se encuentran en `frontend/src/datos.js`. Cada línea de código añadido lleva un comentario explicativo. Las evidencias de ambas partes y las salidas reales de lint y build están en `lab10/evidencias`. La prueba reproducible es `python lab10/verificar.py` (requiere Playwright y Chromium instalados, y Vite en el puerto 5173).

Las siete entidades de la investigación existente son Categoria, Producto, Proveedor, Cliente, Venta, PerfilCliente (OneToOneField) y DetalleVenta (intermedio ManyToManyField). El formulario aplica `ProductoSerializer.validate_precio` de `farmacia_project/src/farmacia/serializers.py`. Guardar en Django requerirá integración HTTP, validación del servidor y persistencia en la API en una etapa posterior.

`node_modules/` y `dist/` permanecen ignorados por Git.

## Laboratorios 11 y 12 — Comunicación entre componentes y AJAX

El frontend conserva las pantallas de los laboratorios anteriores y añade tres vistas: **Productos · API** (gestión conectada a DRF), **Catálogo · Lab 11** (práctica local de carrito) e **Inventario · Lab 10** (interfaz previa). La instancia Axios centraliza `http://127.0.0.1:8000/api/v1` en `frontend/src/api.js`.

Para ejecutar Django, desde `farmacia_project/src`, instala los requisitos y ejecuta `python manage.py runserver`. En otra terminal, desde `frontend`, ejecuta `npm install` y `npm run dev`. CORS autoriza `http://localhost:5173` con `django-cors-headers`.

La gestión usa `GET/POST /productos/`, `GET/PATCH/DELETE /productos/<id>/` y `GET /categorias/`; los filtros envían `search` y `disponible`. La guía de componentes está en [`LAB11_EVIDENCIAS.md`](LAB11_EVIDENCIAS.md) y el informe de AJAX/API está en [`LAB12_EVIDENCIAS.md`](LAB12_EVIDENCIAS.md). Las imágenes organizadas por ejercicio están en [`EVIDENCIAS_LABORATORIOS`](EVIDENCIAS_LABORATORIOS/README.md).

La API conserva `AllowAny` para el laboratorio. CORS controla acceso de lectura desde un origen web; no sustituye autenticación ni permisos para las escrituras.

## Laboratorio 13 — FarmaPoint

FarmaPoint es un panel de gestión de farmacia. El negocio es B2C porque la farmacia vende al consumidor final. El canal cubierto por el panel es la web. Una app móvil o una tienda web pública podrían compartir la API con permisos adecuados.

### Módulos y roles

| Módulo | Estado |
|---|---|
| Catálogo y categorías | API y panel de productos existentes |
| Inventario | Stock de productos existente. Descuento transaccional previsto |
| Clientes y proveedores | Modelos y vistas Django existentes. Pantalla React de clientes prevista |
| Ventas | Modelo Venta y DetalleVenta existentes. API de consulta. Registro mediante el panel React previsto |
| Usuarios, permisos y auditoría | Roles y controles del panel previstos |
| Pagos | Registro del medio y referencia previstos. Integración con pasarela fuera del alcance de esta semana |

| Rol | Permisos previstos | Pantalla |
|---|---|---|
| Visitante | Acceder al ingreso | /login |
| Vendedor | Consultar catálogo, seleccionar cliente y registrar venta | /productos, /clientes, /ventas/nueva |
| Administrador | Administrar catálogo, revisar ventas y controlar accesos | /productos, /ventas |

### Requisitos

| ID | Descripción | Prioridad | Criterio de aceptación |
|---|---|---|---|
| RF01 | Buscar productos por nombre | Alta | Al ingresar un nombre parcial, se muestran solo coincidencias |
| RF02 | Seleccionar el cliente de la venta | Alta | La venta confirmada referencia el cliente seleccionado |
| RF03 | Agregar productos y cantidades | Alta | La pantalla muestra cada línea y su subtotal |
| RF04 | Confirmar una venta | Alta | Con stock suficiente se crea una venta con sus líneas y se descuentan las unidades |
| RF05 | Consultar ventas y su detalle | Media | El operador ve fecha, total y las líneas guardadas |
| RNF01 | Restringir las escrituras por rol | Alta | Una solicitud sin credenciales válidas o sin permiso recibe 401 o 403 y deja intactos los datos |
| RNF02 | Responder con rapidez al consultar productos | Media | Con 500 productos y 10 usuarios simultáneos, el p95 de 100 consultas paginadas es inferior a 500 ms en el entorno de prueba |
| RNF03 | Mantener la consistencia ante fallos | Alta | Si falla una línea en una venta de dos productos, no quedan líneas, venta confirmada ni descuentos parciales |

### Reglas de negocio

| Regla | Capa | Error que evita |
|---|---|---|
| Leer el precio vigente del producto en la base de datos y guardar una copia en el detalle | Django | Precio manipulado o alteración del historial |
| Exigir por lo menos una línea y cantidades enteras positivas | React y Django | Ventas vacías y cantidades incorrectas |
| Validar el stock durante la confirmación y actualizarlo dentro de la misma transacción | Django | Sobreventa y actualizaciones parciales |
| Calcular importes con Decimal y una regla de redondeo a dos decimales | Django | Errores de aritmética monetaria |
| Restringir la confirmación a vendedores y administradores autorizados | Django | Registro de ventas por usuarios sin permiso |

### Arquitectura y flujo

React (pantallas y componentes) → Axios → HTTP/JSON → Django REST Framework (URL, router, vistas y serializadores) → ORM → SQLite. Django devuelve JSON y el código HTTP.

1. React consulta catálogo y muestra stock. Django responde con los datos vigentes. La venta sigue en borrador en la interfaz.
2. El vendedor selecciona el cliente y agrega productos. React presenta los subtotales estimados.
3. React solicita la confirmación. Django comprueba el rol, el cliente, las cantidades y el stock, y calcula los importes con los precios de la base.
4. Django guarda Venta y DetalleVenta y descuenta el stock en una transacción. React muestra la venta registrada o el motivo del rechazo. El endpoint de confirmación es previsto.

Entidades: Venta (principal), DetalleVenta (detalle), Producto, Categoria y Cliente. Los modelos de FarmaPoint ya existen en la app farmacia. Las apps nuevas preparan la organización futura.

### Estructura

~~~text
farmacia_project/src/
  config/settings.py
  core/
  farmacia/
  catalogo/
  clientes/
  ventas/
frontend/src/
  api.js
  components/
  pages/
    ProductosPage.jsx
    ClientesPage.jsx
    VentasPage.jsx
  practica/cafeteria/
    api.js
    components/ProductoCard.jsx
    pages/ProductosPage.jsx
lab13/cafeteria/backend/
  cafeteria/settings.py
  catalogo/
  pedidos/
~~~

### Mapa de rutas

| Recurso | API | Ruta React | Estado |
|---|---|---|---|
| Categorías | /api/v1/categorias/ | /categorias | API existente, pantalla prevista |
| Productos | /api/v1/productos/ | /productos | API existente, panel en / y ruta prevista |
| Clientes | /api/v1/clientes/ | /clientes | Previstos |
| Ventas | /api/v1/ventas/ | /ventas | API de lectura existente, pantalla prevista |
| Confirmación | /api/v1/ventas/ | /ventas/nueva | Escritura y pantalla previstas |

### Verificación local

- En `lab13/cafeteria/backend`, ejecutar `python manage.py check` y `python manage.py runserver 127.0.0.1:8001`.
- En `farmacia_project/src`, instalar las dependencias de `requirements.txt`, ejecutar `python manage.py check` y usar el puerto 8000 para la API del panel.
- En `frontend`, ejecutar `npm ci`, `npm run lint` y `npm run build`.

## Laboratorio 14

Django REST Framework publica las API de catálogo de la cafetería y de ventas de FarmaPoint. El frontend Vite contiene las pantallas de catálogo, listado y detalle. SQLite se crea con las migraciones de cada backend.

| Componente | Archivos o rutas |
|---|---|
| Modelos de cafetería | `lab13/cafeteria/backend/catalogo/models.py`, `pedidos/models.py` |
| API de cafetería | `GET /api/`, CRUD en `/api/productos/`, `POST /api/pedidos/` |
| React de cafetería | `/cafeteria/productos` |
| Modelos de FarmaPoint | `farmacia_project/src/farmacia/models.py`, migración 0004 |
| API de FarmaPoint | `/api/v1/ventas/`, `/api/v1/ventas/<id>/` |
| React de FarmaPoint | `/ventas`, `/ventas/<id>` |

### Ejecutar localmente

1. Instalar dependencias con `python -m pip install -r farmacia_project/src/requirements.txt` desde la raíz.
2. En `farmacia_project/src`, ejecutar `python manage.py migrate`, `python manage.py check` y `python manage.py runserver 127.0.0.1:8000`.
3. En `lab13/cafeteria/backend`, ejecutar `python manage.py migrate`, `python manage.py check` y `python manage.py runserver 127.0.0.1:8001`.
4. En `frontend`, ejecutar `npm ci`, `npm run lint`, `npm run build` y `npm run dev -- --host 127.0.0.1`. Abrir `http://127.0.0.1:5173`.

### Registro de pedidos y ventas

Un POST de pedido o venta recibe un cliente y líneas con producto y cantidad. Ejemplo de estructura JSON, con IDs que deben existir en la base local:

```json
{"cliente": 1, "detalles": [{"producto": 1, "cantidad": 2}]}
```

Django obtiene el precio oficial, calcula el total y usa una actualización condicional con F() para descontar stock dentro de una transacción. Las ventas permiten búsqueda con `?search=`, lectura y edición de cliente y fecha. Los detalles confirmados conservan su precio y cantidad. Eliminar una venta creada por esta API devuelve el stock que descontó. Las ventas históricas se reconocen con `stock_descontado=False`.

### Pago electrónico previsto

La cafetería crea un pago simulado y cambia el pedido a PAGADO dentro de la misma transacción. El módulo real se integrará en la Semana 16. Después de validar el carrito y fijar el importe, Django deberá crear la sesión de pago con el identificador de pedido, importe, moneda y referencias de retorno. El cliente ingresará sus datos en la interfaz de la pasarela.

Django verificará la firma, el importe, la moneda y la referencia de cada notificación antes de actualizar el pedido de forma idempotente. Se conservarán el importe, la moneda, el estado, el identificador de la transacción y su fecha. El número completo, el CVV y el PIN quedan en la pasarela. El pedido comienza PENDIENTE, pasa a PAGADO después de confirmar el cobro y a ENTREGADO al completarse la entrega. Una operación anulada sigue el estado CANCELADO.

En FarmaPoint este paso se ubicaría después de validar la venta y antes de confirmarla como pagada. El API de desarrollo actual registra ventas e inventario y se ejecuta en la interfaz local.

Si el puerto 8000 está ocupado, iniciar FarmaPoint en otro puerto y definir `VITE_FARMAPOINT_API_URL` en `frontend/.env.local`, con el prefijo completo, por ejemplo `http://127.0.0.1:8014/api/v1`.

# Laboratorio 08 — guía de evidencias y pruebas

Implementación sobre `farmacia_project/src/farmacia`, reutilizando los modelos reales. El `QuerySet` personalizado de Semana 7 no estaba presente en el repositorio: para tener la funcionalidad solicitada se añadió `ProductoQuerySet.con_stock()`, que filtra el campo existente `Producto.stock`. No se inventó un estado de producto; para el filtro de estado se usa `Farmacia.estado`.

## Preparación

```powershell
cd .\farmacia_project\src
python -m pip install -r requirements.txt
python manage.py check
python manage.py runserver
```

Para pruebas HTTP se puede usar el navegador DRF, `curl.exe` o extensión REST Client en VS Code. Las URLs base son `http://127.0.0.1:8000/api/v1/` y `http://127.0.0.1:8000/api/v1/basico/`. Los códigos que se deben anotar son los que devuelve el servidor al ejecutarlas; no están precargados en esta guía.

## Ejercicio 1 — instalación y auditoría

**Archivos:** `config/settings.py`, `requirements.txt` y `farmacia/models.py`.

**Capturas:**

- `capturas/ejercicio01/E01_C01_dependencias.png`: `src/requirements.txt`, con Django y Django REST Framework.
- `capturas/ejercicio01/E01_C02_installed_apps.png`: `rest_framework` y `farmacia` dentro de `INSTALLED_APPS`.
- `capturas/ejercicio01/E01_C03_verificacion.png`: terminal ejecutando `pip show djangorestframework` y `python manage.py check`, con resultados reales.
- `capturas/ejercicio01/E01_C04_modelos.png`: modelos `Categoria`, `Producto`, `Farmacia` y campo `estado`; la implementación del QuerySet nuevo se identifica como adaptación.

**Justificación:** DRF queda habilitado en el proyecto existente y se identifican sus recursos a partir de los modelos reales.

## Ejercicio 2 — serializadores

**Archivo:** `farmacia/serializers.py`. El `ProductoSerializer` representa un producto y una lista; `many=True` convierte el QuerySet en una colección serializable.

En `python manage.py shell`, usando una categoría existente:

```python
from farmacia.models import Categoria, Producto
from farmacia.serializers import ProductoSerializer

producto = Producto.objects.select_related('categoria').first()
ProductoSerializer(producto).data
ProductoSerializer(Producto.objects.select_related('categoria').all(), many=True).data
```

**Capturas:**

- `capturas/ejercicio02/E02_C01_serializer_objeto.png`: shell con `ProductoSerializer(producto).data` y la salida real.
- `capturas/ejercicio02/E02_C02_serializer_queryset.png`: shell con `many=True` y la salida real de lista.

**Justificación:** el `ModelSerializer` convierte instancias del ORM a estructuras que DRF puede representar como JSON.

## Ejercicio 3 — validación propia

**Archivo:** `farmacia/serializers.py`, método `validate_precio`. La validación rechaza precios iguales o menores a cero.

En shell, sustituye el ID por una categoría existente. El bloque atómico permite demostrar `save()` y revierte la fila de demostración al terminar:

```python
from django.db import transaction
from rest_framework.serializers import ValidationError
from farmacia.serializers import ProductoSerializer

datos = {'nombre': 'Producto de demostración', 'descripcion': '', 'precio': '3.50', 'stock': 1, 'categoria': 1}
serializador = ProductoSerializer(data=datos)
serializador.is_valid(), serializador.validated_data, serializador.errors
try:
    with transaction.atomic():
        serializador.save()
        raise RuntimeError('ROLLBACK_DEMO')
except RuntimeError as error:
    if str(error) != 'ROLLBACK_DEMO':
        raise

datos_invalidos = {**datos, 'precio': '0'}
invalido = ProductoSerializer(data=datos_invalidos)
invalido.is_valid(), invalido.errors
```

**Capturas:**

- `capturas/ejercicio03/E03_C01_valido.png`: resultado real de `is_valid()` y `validated_data`.
- `capturas/ejercicio03/E03_C02_save.png`: llamada a `save()` dentro del bloque y ejecución completa sin error distinto al rollback de demostración.
- `capturas/ejercicio03/E03_C03_invalido.png`: `is_valid()` falso y error real del campo `precio`.

**Justificación:** la validación de campo da un mensaje claro antes de guardar datos inválidos.

## Ejercicio 4 — vistas genéricas

**Archivos:** `farmacia/api_generic_views.py`, `farmacia/api_generic_urls.py` y `config/urls.py`.

- `GET`/`POST`: `http://127.0.0.1:8000/api/v1/basico/productos/`
- `GET`/`PUT`/`PATCH`/`DELETE`: `http://127.0.0.1:8000/api/v1/basico/productos/ID/`

**Capturas:**

- `capturas/ejercicio04/E04_C01_lista.png`: navegador en la URL de lista mostrando respuesta DRF real.
- `capturas/ejercicio04/E04_C02_detalle.png`: navegador en el detalle de un ID existente.

**Justificación:** las vistas genéricas implementan operaciones de colección y detalle con poco código y los serializers existentes.

## Ejercicio 5 — ViewSet y router

**Archivos:** `farmacia/api_views.py`, `farmacia/api_urls.py`, `config/urls.py`.

El router registra `productos`, `categorias`, `farmacias` y `ventas`. La colección de productos está en `http://127.0.0.1:8000/api/v1/productos/`.

**Capturas:**

- `capturas/ejercicio05/E05_C01_router.png`: `api_urls.py` mostrando el `DefaultRouter` y registros.
- `capturas/ejercicio05/E05_C02_productos.png`: navegador en el endpoint de productos.

**Justificación:** el router genera las rutas estándar del CRUD para cada `ModelViewSet`.

## Ejercicio 6 — métodos HTTP y respuestas

Probar contra `/api/v1/productos/` y `/api/v1/productos/ID/`. Para crear un producto, enviar JSON con un `categoria` existente; por ejemplo:

```json
{"nombre":"Prueba API","descripcion":"Temporal","precio":"2.50","stock":1,"categoria":1}
```

Probar colección `GET`, `POST` válido, `POST` con `precio: "0"`, detalle `PUT` o `PATCH`, `DELETE` sobre el registro creado en esta prueba y después `GET` a ese ID. Registrar el estado HTTP que efectivamente muestre el cliente para cada petición. Crear y eliminar únicamente el registro temporal de prueba.

PowerShell (reemplaza `categoria` por un ID existente; el POST válido crea el registro temporal que luego elimina este mismo bloque):

```powershell
$base = 'http://127.0.0.1:8000/api/v1/productos/'
$categoriaId = 1
$json = @{ nombre='Prueba API temporal'; descripcion=''; precio='2.50'; stock=1; categoria=$categoriaId } | ConvertTo-Json
$creado = Invoke-WebRequest -Method Post -Uri $base -ContentType 'application/json' -Body $json
$creado.StatusCode
$id = ($creado.Content | ConvertFrom-Json).id
$invalido = @{ nombre='Precio inválido'; descripcion=''; precio='0'; stock=1; categoria=$categoriaId } | ConvertTo-Json
try { Invoke-WebRequest -Method Post -Uri $base -ContentType 'application/json' -Body $invalido } catch { $_.Exception.Response.StatusCode.value__ }
Invoke-WebRequest -Method Patch -Uri "$base$id/" -ContentType 'application/json' -Body (@{ stock=2 } | ConvertTo-Json) | Select-Object -ExpandProperty StatusCode
Invoke-WebRequest -Method Delete -Uri "$base$id/" | Select-Object -ExpandProperty StatusCode
try { Invoke-WebRequest -Uri "$base$id/" } catch { $_.Exception.Response.StatusCode.value__ }
```

**Capturas:**

- `capturas/ejercicio06/E06_C01_get_post.png`: petición GET y POST válido con respuesta/códigos reales.
- `capturas/ejercicio06/E06_C02_post_invalido.png`: POST inválido y detalle de validación.
- `capturas/ejercicio06/E06_C03_patch.png`: PATCH o PUT con código y cuerpo reales.
- `capturas/ejercicio06/E06_C04_delete_404.png`: DELETE del registro temporal, seguido de GET al mismo ID inexistente; anotar ambos estados.

**Justificación:** las pruebas permiten observar cómo el API traduce métodos HTTP a operaciones CRUD y errores de validación o búsqueda.

## Ejercicio 7 — respuesta anidada y consultas

**Archivos:** `farmacia/serializers.py`, `farmacia/api_views.py`. `VentaReadSerializer` incluye el cliente y detalles; cada detalle incluye su producto. El QuerySet usa `select_related('cliente')` y `prefetch_related('detalles__producto__categoria')`.

URL: `http://127.0.0.1:8000/api/v1/ventas/`. Para comparar consultas, usa el shell con datos disponibles:

```python
from django.db import connection, reset_queries
from django.test.utils import CaptureQueriesContext
from farmacia.models import Venta
from farmacia.serializers import VentaReadSerializer

with CaptureQueriesContext(connection) as antes:
    VentaReadSerializer(Venta.objects.all(), many=True).data
with CaptureQueriesContext(connection) as despues:
    qs = Venta.objects.select_related('cliente').prefetch_related('detalles__producto__categoria')
    VentaReadSerializer(qs, many=True).data
len(antes), len(despues)
```

Los conteos dependen de la cantidad y relaciones de los datos. En la prueba automatizada aislada con una venta y un detalle, la serialización ingenua ejecuta 5 consultas y el QuerySet optimizado 4. Para la captura de shell, registra los conteos que produzca la base local.

**Capturas:**

- `capturas/ejercicio07/E07_C01_json_anidado.png`: respuesta de ventas con cliente, detalles y producto anidados.
- `capturas/ejercicio07/E07_C02_consultas.png`: shell mostrando las dos cantidades medidas en la base local.
- `capturas/ejercicio07/E07_C03_optimizacion.png`: fragmento del QuerySet optimizado de `VentaReadOnlyViewSet`.

**Justificación:** las relaciones anidadas presentan la información relacionada en una sola respuesta y la carga anticipada reduce consultas repetidas.

## Ejercicio 8 — búsqueda, orden y filtros

La colección `/api/v1/productos/` acepta `?search=texto`, `?ordering=precio` o `?ordering=-stock` y `?disponible=true|false`. `/api/v1/farmacias/` acepta `?estado=VALOR`, `?search=texto` y `?ordering=nombre`. La acción `/api/v1/productos/con-stock/` reutiliza `Producto.objects.con_stock()`.

URLs de ejemplo (los valores deben existir en tus datos):

1. `/api/v1/productos/?search=vitamina`
2. `/api/v1/farmacias/?estado=ACTIVA`
3. `/api/v1/productos/?search=analgesico&ordering=-precio&disponible=true`
4. Acción: `/api/v1/productos/con-stock/`

**Capturas:** `capturas/ejercicio08/E08_C01_busqueda.png`, `E08_C02_filtro_estado.png`, `E08_C03_combinacion.png`, `E08_C04_accion_queryset.png`: mostrar cada URL y su respuesta real. El valor `ACTIVA` es solo ejemplo de parámetro; utilizar el valor que exista en los registros.

**Justificación:** los filtros se basan en campos existentes y la acción personalizada reutiliza una consulta de disponibilidad.

## Ejercicio 9 — entidades de la investigación

Las siete entidades que el README identifica como investigación son `Categoria`, `Producto`, `Proveedor`, `Cliente`, `PerfilCliente`, `Venta` y `DetalleVenta`. Relaciones: Categoria 1:N Producto; Cliente 1:1 PerfilCliente; Cliente 1:N Venta; Venta N:M Producto a través de DetalleVenta. Recursos: `Categoria` es simple y `Venta` es anidado. El campo de estado del proyecto de ubicaciones es `Farmacia.estado`. No había método personalizado de Semana 7; se documenta la adaptación `ProductoQuerySet.con_stock()`.

**Capturas:** `capturas/ejercicio09/E09_C01_siete_entidades.png` (modelos) y `E09_C02_relaciones_estado.png` (relaciones/campos y auditoría en este documento).

**Justificación:** la selección de entidades y relaciones procede de los modelos y del README existentes.

## Ejercicio 10 — tres serializers y validación

`CategoriaSerializer`, `ProductoSerializer` y `ClienteSerializer` cubren tres recursos. La validación personalizada está en `ProductoSerializer.validate_precio`; la demostración de válido/inválido está en el ejercicio 3.

**Capturas:** `capturas/ejercicio10/E10_C01_tres_serializers.png` (clases en `serializers.py`) y `E10_C02_validacion.png` (salida real válida e inválida del shell).

**Justificación:** varios recursos cuentan con representación explícita y el precio se valida antes de persistir.

## Ejercicio 11 — router de dos recursos y códigos

`CategoriaViewSet` y `ProductoViewSet` ofrecen `ModelViewSet`. Usar un producto/categoría temporal: probar GET (`200`), POST válido (`201`), POST con precio inválido (`400`), GET de ID inexistente (`404`) y DELETE del temporal (`204`). Confirmar esos códigos en la respuesta del cliente.

**Capturas:** `capturas/ejercicio11/E11_C01_get_200.png`, `E11_C02_post_201.png`, `E11_C03_post_400.png`, `E11_C04_get_404.png`, `E11_C05_delete_204.png`.

**Justificación:** los estados HTTP esperados distinguen lecturas, creaciones, errores de validación, recursos ausentes y eliminaciones exitosas; incluir los códigos medidos.

## Ejercicio 12 — recurso anidado de solo lectura

`VentaReadOnlyViewSet` presenta venta, cliente, detalles y productos relacionados. `ReadOnlyModelViewSet` expone solamente lectura; el QuerySet optimiza con `select_related` y `prefetch_related`. La comparación de consultas se ejecuta en el ejercicio 7.

**Capturas:** `capturas/ejercicio12/E12_C01_read_only.png` (clase ViewSet y router) y `E12_C02_relaciones_consulta.png` (JSON más conteos medidos).

**Justificación:** las ventas se exponen sin permitir cambios por API y las relaciones se cargan anticipadamente.

## Ejercicio 13 — filtros y acción personalizada

Usa búsquedas, ordenamiento y filtro de estado de los ejercicios 5/8. URLs de ejemplo: `/api/v1/productos/?search=vitamina`, `/api/v1/farmacias/?estado=ACTIVA&ordering=nombre`, `/api/v1/productos/?disponible=true&ordering=-precio`; acción `/api/v1/productos/con-stock/`. Sustituye los valores por términos y estados presentes.

**Capturas:** `capturas/ejercicio13/E13_C01_busqueda.png`, `E13_C02_estado_orden.png`, `E13_C03_combinacion.png`, `E13_C04_accion.png`.

**Justificación:** la API permite componer filtros de campos existentes y reusa el QuerySet de disponibilidad.

## Ejercicio 14 — documentación y verificación

Se actualizaron los dos `requirements.txt`, este README y `farmacia_project/README.md`. Verificación completada desde `farmacia_project/src`: `python manage.py check` sin problemas, `python manage.py test farmacia` con 19 pruebas exitosas y `python manage.py makemigrations --check --dry-run` sin cambios de esquema. No se hicieron commits ni push.

**Capturas:** `capturas/ejercicio14/E14_C01_requirements_readme.png` (dependencias y sección Lab 08), `E14_C02_check_tests.png` (salida completa real de los comandos), `E14_C03_git_status.png` (lista de cambios pendientes, sin commit).

**Justificación:** dependencias, uso y evidencias quedan documentados; los cambios quedan listos para revisión antes de cualquier commit o push.

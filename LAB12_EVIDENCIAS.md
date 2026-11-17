# Laboratorio 12 — AJAX y servicios web

## Adaptación y estado

Se integró la gestión de productos con la API versionada que ya existe en `farmacia_project/src`: `http://127.0.0.1:8000/api/v1/`. El mini catálogo de `src/practica/` sigue siendo el ejercicio local del Laboratorio 11. El panel de gestión ahora carga y modifica datos del servidor.

Para ejecutar, instala dependencias Django y npm si todavía no lo hiciste. Inicia `python manage.py runserver` desde `farmacia_project/src` y `npm run dev` desde `frontend`, en terminales distintas. `django-cors-headers` se agregó a `requirements.txt`; `corsheaders` está en `INSTALLED_APPS` y `CorsMiddleware` precede a `CommonMiddleware`. El origen autorizado es `http://localhost:5173`.

La instancia `src/api.js` centraliza `baseURL: http://127.0.0.1:8000/api/v1` y timeout de 10 segundos. No repetir la URL en componentes.

## Estructura y datos confirmados en el backend

| Dato | Implementación real |
| --- | --- |
| Modelo | `Producto`: nombre, descripción, precio, stock, categoría |
| Serializer | `ProductoSerializer`; incluye `id`, los campos anteriores y `categoria_nombre` de solo lectura |
| Alta/edición | `categoria` es la clave primaria de una categoría existente; el formulario obtiene opciones de `GET /categorias/` |
| Validación | `validate_precio`: precio debe ser mayor que cero |
| Lista y detalle | `GET /productos/`, `GET /productos/<id>/` |
| Alta y edición | `POST /productos/`, `PATCH /productos/<id>/` |
| Eliminación | `DELETE /productos/<id>/` |
| Búsqueda | `?search=...`, por nombre, descripción y nombre de categoría |
| Disponibilidad | `?disponible=true` o `?disponible=false` |
| Orden | `?ordering=precio` (también nombre y stock) |
| Acción | `/productos/con-stock/` |

El backend ya tenía CRUD, filtros, acción, serializer y permiso DRF predeterminado `AllowAny`; no fue necesario cambiar esas vistas. El panel utiliza carga cancelable con `AbortController`, estados de carga/error/lista vacía, mensajes de validación de DRF, POST, PATCH y DELETE con confirmación. El resumen se calcula a partir de los productos que devuelve la API. La lista se vuelve a consultar al cambiar texto o disponibilidad.

En el entorno de edición no fue posible instalar paquetes desde PyPI/npm por bloqueo de red. Por ello `manage.py check`, `npm run lint` y `npm run build` quedan pendientes hasta ejecutar las instalaciones indicadas en Preparación. La sintaxis de `settings.py`, el JSON de `package.json` y `src/api.js` sí se comprobaron localmente.

## Tabla de operaciones y respuestas esperadas

| Operación | Método y ruta | Código normal |
| --- | --- | --- |
| Listar / filtrar | `GET /api/v1/productos/` | 200 |
| Obtener uno | `GET /api/v1/productos/<id>/` | 200, 404 si no existe |
| Crear | `POST /api/v1/productos/` | 201, 400 por validación |
| Editar parcialmente | `PATCH /api/v1/productos/<id>/` | 200, 400 por validación |
| Reemplazar completo | `PUT /api/v1/productos/<id>/` | 200, 400 por validación |
| Eliminar | `DELETE /api/v1/productos/<id>/` | 204, 404 si no existe |

El serializer requiere los campos del modelo que no son opcionales, incluyendo `categoria` como ID; `descripcion` puede quedar vacía. El formulario manda precio como decimal textual, stock como entero y categoría como ID. Deja que el precio `0` llegue al servidor para observar el POST 400 del serializer; el error devuelto queda visible junto al formulario.

## URLs de búsqueda para registrar

Usa nombres existentes en la base de datos y copia los resultados reales observados en el documento de entrega:

- `/api/v1/productos/?search=Analgesico`
- `/api/v1/productos/?disponible=true`
- `/api/v1/productos/?search=Analgesico&disponible=true`

El backend usa `SearchFilter` con búsqueda parcial; `disponible=true` conserva productos con stock mayor que cero. Las capturas del Word deben mostrar las URLs y resultados reales de tu base.

## Conceptos para explicar

React inicia una acción; Axios envía una solicitud HTTP; el Router la dirige al ViewSet; el serializer transforma y valida la entrada/salida; el ORM consulta o cambia SQLite; Django devuelve JSON y un código HTTP; el componente actualiza su estado. A diferencia de AJAX, que recibe datos para que React actualice una parte de la pantalla, una vista Template devuelve HTML renderizado por Django.

CORS permite al navegador leer respuestas del servidor desde un origen explícitamente autorizado. No es autenticación ni autorización. En esta práctica las escrituras siguen públicas por `AllowAny`; antes de producción deben configurarse autenticación y permisos apropiados.

## Evidencias que requieren ejecución local

El código está preparado para las pruebas, pero las capturas de Network, del error CORS inicial, de respuestas HTTP y de la consola deben hacerse con ambos servidores en ejecución y una base con datos. No se incluyen respuestas o JSON inventados. Captura como mínimo:

1. API GET en navegador, URL, código 200 y un fragmento del JSON real.
2. Prueba CORS previa (si se reproduce) y posterior, `settings.py` y `requirements.txt`.
3. `api.js`, `package.json` y GET 200 en Network.
4. Estados cargando, error (detén Django), lista vacía y lista con registros.
5. Alta válida POST 201 y precio inválido POST 400 con el cuerpo real del error.
6. Edición PATCH 200 y eliminación confirmada DELETE 204, antes y después.
7. URL de búsqueda, filtro de disponibilidad y combinación; Network debe mostrar params reales.
8. `npm run lint`, `npm run build`, `git status`; verificar que `node_modules/`, `dist/` y bases locales no estén versionadas.

## Conclusión para redactar con palabras propias

Explica el intercambio HTTP/JSON de React con Django, el propósito de Axios y `baseURL`, CORS en desarrollo local, los estados de carga/error/vacío, cómo se reflejan POST/PATCH/DELETE en el estado, los parámetros de filtro y por qué hacen falta autenticación y permisos antes de producción.

No se ejecutaron commit ni push.

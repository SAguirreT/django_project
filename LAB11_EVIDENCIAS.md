# Laboratorio 11 — Comunicación entre componentes

## Estado de implementación

El repositorio original no incluía `frontend/`. Se agregó un proyecto Vite/React independiente en la raíz del repositorio. Ambas pantallas usan datos locales, en memoria, y no envían solicitudes a la API. Ejecutar desde `frontend/` con `npm install` y `npm run dev`; lint y build se ejecutan con `npm run lint` y `npm run build`.

## Parte 1 — Mini catálogo

`src/practica/datos.js` exporta los cinco productos de ejemplo con precio como texto. `Practica.jsx` es el padre de `Catalogo` y `Carrito`; guarda líneas del carrito y búsqueda. `Catalogo` usa `map()` con `key` estable y pasa cada producto a `ProductoCard`. La tarjeta presenta precio con dos decimales, existencia y botón deshabilitado si no hay stock.

### Tabla de props

| Prop | Tipo | La define | La recibe |
| --- | --- | --- | --- |
| `productos` | Arreglo de objetos | `Practica` | `Catalogo` |
| `producto` | Objeto | `Catalogo`, por elemento | `ProductoCard` |
| `onAgregar` | Función `(producto) => void` | `Practica` | `Catalogo`, `ProductoCard` |
| `lineas` | Arreglo de líneas `{id, nombre, precio, cantidad}` | `Practica` | `Carrito` |
| `onQuitar` | Función `(id) => void` | `Practica` | `Carrito` |
| `onVaciar` | Función `() => void` | `Practica` | `Carrito` |
| `valor` | Texto | `Practica` | `Buscador` |
| `onCambiar` | Función `(texto) => void` | `Practica` | `Buscador` |
| `mensaje` | Texto | `Practica` | `Aviso` |
| `onCerrar` | Función `() => void` | `Practica` | `Aviso` |

Las props son de solo lectura para el hijo: el hijo no modifica el objeto recibido. El padre actualiza estado creando objetos y arreglos nuevos. El `context` que una View Django entrega a un Template es comparable como mecanismo para entregar datos de renderizado, aunque no es el sistema de props de React.

`agregarAlCarrito` recibe el callback de la tarjeta; se pasa como función y el clic lo invoca. Las líneas existentes se incrementan con `map()` y las nuevas se agregan con spread. Quitar usa `filter()` y vaciar asigna `[]`. Unidades y total se derivan con `reduce()`, no se duplican en estado. El carrito cambia `document.title` según unidades. `Aviso` se cierra tras tres segundos y limpia su temporizador al cambiar o desmontar.

### Búsquedas y cálculo para verificar

- Buscar `ca`: debe listar Café americano, Capuchino y Torta de chocolate.
- Buscar `zzz`: debe mostrar «No hay productos que coincidan».
- Agregar dos Capuchinos y un Café americano: 3 unidades, total S/ 24.50.
- El producto sin stock muestra «Agotado» y su botón no responde.

## Parte 2 — Panel de FarmaPoint

### Equivalencia y árbol

| Elemento | Aplicación |
| --- | --- |
| Entidad principal | Producto |
| Componente padre | `PanelProductos.jsx` |
| Listado | `ListaProductos.jsx` |
| Fila | `ProductoFila.jsx` |
| Formulario de alta | `FormularioProducto.jsx` |
| Resumen hermano | `ResumenProductos.jsx` |
| Buscador | `BuscadorProductos.jsx` |
| Campo de búsqueda | Nombre del producto |

```text
PanelProductos (productos, búsqueda)
├── BuscadorProductos (valor, onCambiar)
├── ResumenProductos (productos)
├── FormularioProducto (onGuardar)
└── ListaProductos (productos filtrados, onEliminar, onCambiarEstado)
    └── ProductoFila (producto, onEliminar, onCambiarEstado)
```

El modelo Django `Producto` define `nombre`, `descripcion`, `precio`, `stock` y `categoria` (FK a `Categoria`). `ProductoForm` usa esos cinco campos; precio es Decimal con dos decimales y stock es entero no negativo. Los registros del panel conservan `precio` como texto. La categoría de ejemplo se representa como etiqueta de texto porque el ejercicio es local y no conecta ni solicita la lista de categorías de la API.

El estado del padre contiene cinco registros iniciales. Eliminar actualiza con `filter()`; cambiar disponibilidad actualiza con `map()`; el alta agrega un registro mediante spread. El resumen deriva el conteo, stock acumulado y cantidad disponible. El buscador recibe valor y callback y filtra por nombre. El título del documento se actualiza con un efecto dependiente de la cantidad de productos.

El formulario controla los campos nombre, descripción, precio, stock y categoría. Rechaza nombre vacío, precio no numérico/no positivo o categoría vacía; stock vacío se guarda como cero, consistente con `PositiveIntegerField`. Caso válido: `Ibuprofeno 400 mg`, precio `12.50`, stock `15`, categoría `Medicamentos`. Caso inválido: nombre vacío y precio `0`, se presenta el primer mensaje de validación y no se agrega.

## useEffect y limpieza

- `useEffect(() => {}, [])` se ejecuta al montar; StrictMode puede repetir el ciclo de comprobación en desarrollo.
- `useEffect(() => {}, [cantidad])` se ejecuta al montar y cuando cambia `cantidad`.
- `useEffect(() => {})` se ejecuta después de cada render.
- La limpieza de `Aviso` cancela el temporizador anterior al actualizar el efecto o desmontar el componente.
- StrictMode puede ejecutar efectos otra vez en desarrollo para detectar efectos secundarios no seguros.

## Capturas ilustrativas y evidencias pendientes

Se generaron tres mockups PNG genéricos en `capturas_lab11/`: gestión de productos, catálogo con carrito de 3 unidades y búsqueda sin coincidencias. Cada imagen lleva una marca visible de **SIMULACIÓN VISUAL · evidencia genérica**. No son capturas de una ejecución real del frontend; sirven como apoyo visual de referencia.

- `capturas_lab11/01_panel_productos.png`
- `capturas_lab11/02_catalogo_carrito.png`
- `capturas_lab11/03_busqueda_sin_resultados.png`

El script `capturas_lab11/generar_mockups.ps1` las vuelve a generar. Para el Word todavía se necesitan capturas de ejecución real de código, navegador y terminal. Guardar además:

1. `datos.js`, `Practica.jsx`, `Catalogo.jsx`, `ProductoCard.jsx` y catálogo en navegador.
2. Tabla de props y explicación de props inmutables.
3. Clic en Agregar y consola mostrando el nombre del producto.
4. Carrito con 3 unidades y S/ 24.50; quitar y vaciar.
5. Búsqueda `ca` y búsqueda `zzz`.
6. Título de pestaña, aviso temporal y código de limpieza.
7. Tabla de equivalencias y árbol de componentes.
8. Panel, acciones de disponibilidad/eliminación, formulario válido e inválido, resumen y filtros.
9. Terminal con lint, build, git status y URL del repositorio.

Las conclusiones finales deben redactarse con palabras propias: paso padre-hijo mediante props; callbacks del hijo al padre; estado elevado compartido por hermanos; valores derivados sin duplicación; efectos y limpieza; aplicación en el panel local.

No se realizaron commit ni push. El repositorio indicado por la guía es https://github.com/SAguirreT/django_project.

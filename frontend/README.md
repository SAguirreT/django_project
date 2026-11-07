# FarmaPoint — Laboratorio 10

El frontend reorganiza los datos locales de Semana 9 en componentes funcionales. La investigación propia ya documentada utiliza Categoria, Producto, Proveedor, Cliente, Venta, PerfilCliente (1:1) y DetalleVenta (intermedio M:N); ambas partes tienen listas y formularios independientes con los mismos datos iniciales.

```bash
npm install
npm run dev
npm run lint
npm run build
```

Usar Node.js 22.12+; verificado con Node 24. La URL local es http://localhost:5173/.

- `App.jsx`: organiza ambas partes y pasa únicamente datos.
- `datos.js`: conserva productos, categorías y ventas del laboratorio anterior.
- `components/Tarjeta.jsx`: recibe título y children.
- `components/ProductoCard.jsx`: muestra props, valor por defecto y reservas locales limitadas por stock.
- `components/ListaProductos.jsx`: búsqueda controlada, categorías y formulario con onSubmit, preventDefault y actualización inmutable; reproduce la regla de precio positivo del serializer de Django.
- `components/VentaCard.jsx`: compone detalles y calcula el total.
- `components/DetalleItem.jsx`: muestra cada línea del modelo intermedio.
- `components/Investigacion.jsx`: presenta la Parte 2 con estado independiente.

No se pasan funciones entre componentes ni se consume la API. Los registros nuevos se pierden al recargar; la persistencia requerirá POST a Django y manejar autenticación, respuestas y validación del servidor. Los comentarios explican cada línea añadida. Las capturas reales y comprobaciones están en `../lab10/evidencias`; node_modules y dist no se versionan.

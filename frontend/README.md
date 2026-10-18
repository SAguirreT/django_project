# FarmaPoint · Frontend React (Lab 09)

Integrantes: Dario Maza, Sheila Aguirre y Jose Contreras.

## Instalar y ejecutar

Requiere Node.js 24 LTS y npm. Desde la raíz del repositorio:

```powershell
cd frontend
npm install
npm run dev
```

Abrir http://localhost:5173/. Para una instalación reproducible usar `npm ci`.

```powershell
npm run lint
npm run build
npm run preview
```

La plantilla actual utiliza Oxlint para `lint`. Vite carga su configuración mediante el cargador nativo de Node para evitar archivos de configuración temporales. `dist/` se genera al compilar; no se publica en Git.

## Qué muestra

Cinco productos, tres categorías y dos ventas con detalles. Búsqueda por nombre, filtro por categoría, stock disponible/agotado, aviso de pocas unidades y mensaje de lista vacía. Los totales se calculan a partir de cantidad y precio unitario; las ventas de demostración suman S/ 27.90 y S/ 24.00.

Los arreglos están escritos en `src/App.jsx` y conservan los campos de ProductoSerializer, CategoriaSerializer y VentaReadSerializer del Lab 08. Los precios son cadenas. Este laboratorio no consume la API ni cambia la base de datos. La relación Venta -> DetalleVenta -> Producto usa mapas anidados con claves id. Las siete entidades de la investigación son Categoria, Producto, Proveedor, Cliente, Venta, PerfilCliente (1:1) y DetalleVenta (intermedio M:N).

## Demostración al profesor

1. Buscar un nombre inexistente para mostrar «No hay registros» y limpiar filtros.
2. Seleccionar Higiene: aparecen dos productos.
3. Ver Ibuprofeno agotado; Alcohol y Mascarillas muestran pocas unidades.
4. Revisar las ventas: 2 × 5.50 + 12.00 + 4.90 = 27.90; 2 × 12.00 = 24.00.
5. Editar el nombre de un producto en App.jsx: Vite actualiza la página.
6. Para probar el arreglo realmente vacío, guardar una copia y sustituir temporalmente productos por []; restaurar después.

El PDF, las capturas y los registros de ejecución se encuentran en `../lab09/`. Los datos son ficticios.

En este entorno Windows se comprobó npm con `npm_config_script_shell` apuntando a PowerShell, porque el lanzador CMD no completaba la ejecución. Este ajuste es local y no se impone a otros sistemas.

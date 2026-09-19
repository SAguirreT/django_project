# Guía de evidencias del Laboratorio 05

Esta guía identifica las evidencias pendientes. Las pruebas automáticas no
sustituyen las capturas del navegador solicitadas por el docente. Completar las
respuestas en el Word original con resultados observados, no con resultados
supuestos. Si la Parte 1 corresponde a otra aplicación del Lab 04, documentarla
por separado: este paquete cubre el proyecto de farmacia inspeccionado.

## Ejercicios 1 a 3 y 9

- Identificar las cinco entidades originales: Categoria, Producto, Proveedor,
  Cliente y Venta; y las añadidas: PerfilCliente y DetalleVenta.
- Explicar Cliente–PerfilCliente (1:1), Categoria–Producto y Cliente–Venta (1:N),
  y Venta–Producto a través de DetalleVenta (N:M).
- Capturar `python manage.py showmigrations farmacia`, la sesión iniciada en
  `/admin/` y los siete registros explícitos al final de `farmacia/admin.py`.
- El acceso ya existente al administrador permite reutilizar el superusuario.
  No incluir contraseñas en el informe.

## Ejercicios 4, 5 y 10

Capturar las clases ProductoAdmin, ClienteAdmin y VentaAdmin, y sus listados en
el navegador. En Productos, buscar un producto por nombre y luego seleccionar
una categoría en el filtro lateral. Capturar ambos resultados. En Ventas,
mostrar las columnas de cliente, fecha y total y los filtros por fecha.

## Ejercicios 6 y 11 — Relación 1:1

Capturar PerfilClienteInline y ClienteAdmin. Abrir Clientes → Añadir cliente:
el perfil aparece dentro del formulario del cliente. Crear un cliente temporal
con una dirección de prueba, guardar y volver a abrirlo. Modificar la dirección,
guardar y reabrir para confirmar persistencia. Capturar cada resultado. Para
eliminar solo el perfil, marcar Eliminar en el inline y guardar: el cliente
permanece. No borrar registros reales para esta demostración.

## Ejercicios 7 y 12 — Relación N:M

Capturar DetalleVentaInline y VentaAdmin. Crear una venta temporal para el
cliente de prueba y añadir un producto en el inline con cantidad 2 y precio
unitario 12.50. Introducir total 25.00. Guardar y reabrir. Cambiar cantidad a 3
y total a 37.50, guardar y reabrir. Capturar la tabla de detalles antes y después.
Marcar Eliminar en ese detalle, ajustar el total a 0.00 y guardar. Confirmar
que la venta permanece y que el detalle ha desaparecido.

El total de Venta no se recalcula automáticamente y el stock no se modifica al
guardar los detalles: esas reglas no estaban implementadas en el proyecto y no
forman parte de la personalización exigida.

## Ejercicios 8 y 13 — Flujo completo

Para la relación 1:N, crear un producto temporal asociado a una categoría,
editar su stock y eliminar ese producto. Capturar creación, modificación y
confirmación de eliminación. Conservar la categoría.

Para cada relación, verificar persistencia volviendo a abrir el registro tras
guardar. Opcionalmente comprobarlo mediante el ORM desde `manage.py shell`.
Las pruebas automáticas realizan operaciones equivalentes en una base SQLite
de pruebas, sin modificar la base de datos del usuario.

Justificación orientativa que debes adaptar con tus palabras: el Admin permite
al personal autorizado gestionar los modelos y sus relaciones sin desarrollar
formularios internos desde cero. Reutiliza los modelos y el ORM. La interfaz
de FarmaPoint sigue necesitando sus vistas y plantillas para presentar la
navegación y los flujos orientados al usuario final.

## Ejercicio 14 y entrega

1. Ejecutar `python manage.py check` y `python manage.py test farmacia`.
2. Revisar README.md, requirements.txt, admin.py y test_admin.py.
3. Revisar `git diff` antes de seleccionar los cambios para el commit; el
   repositorio ya tenía modificaciones locales ajenas a este paquete.
4. Hacer commit y push desde el repositorio cuando la revisión esté completa.
5. Incluir en el Word la URL real del repositorio, las respuestas de los 14
   ejercicios, capturas solicitadas y conclusiones propias.

El instalador no hace commit ni push, no crea capturas y no modifica el Word.

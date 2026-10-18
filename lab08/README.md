# Entrega del Laboratorio 08

Integrantes: Dario Maza, Sheila Aguirre y Jose Contreras.

- `Informe_Lab08_FarmaPoint.pdf`: informe de 44 páginas, 14 ejercicios, justificaciones y evidencias.
- `INFORME.md`: respuestas editables y referencias a las imágenes.
- `evidencias/`: 69 capturas PNG, respuestas JSON y registros de comprobación.
- `FarmaPoint_Lab08.postman_collection.json`: colección para reproducir el CRUD. Ajustar las variables de categoría y zona si no se usa la base ficticia limpia.
- `recolectar.py`: ejecuta las peticiones HTTP y compara las consultas de serialización.
- `capturar.cjs`: captura archivos/resultados en un visor y páginas reales de DRF; requiere Playwright y Edge.
- `generar_informe.py`: reconstruye el informe con ReportLab y Pillow en Windows.

## Reproducción de la base de evidencias

Desde la raíz del repositorio, con el entorno virtual activado:

```powershell
$env:FARMAPOINT_DB = Join-Path (Get-Location) 'lab08/demo.sqlite3'
python farmacia_project/src/manage.py migrate
python farmacia_project/src/manage.py sembrar_lab08
python lab08/recolectar.py
```

El servidor local utiliza el puerto 8008. La base de demostración queda excluida de Git. El script crea y elimina exclusivamente registros temporales propios, además de utilizar los datos LAB08 sembrados. Se recomienda una base nueva para reproducir exactamente los IDs y los conteos publicados.

## Alcance de las capturas

Los resultados HTTP se obtuvieron mediante urllib, no desde Postman/Thunder Client. Las imágenes de código y resultados son capturas de un visor que muestra archivos reales. Se incluyen cuatro capturas directas del navegador en DRF y HTML. Si el docente exige la interfaz exacta de Postman, importar la colección y repetir las solicitudes allí.

## Verificación

- Versión pública: 25 pruebas correctas; sin migraciones pendientes de generar.
- Copia local con cambios previos de Semana 7: 32 pruebas correctas.
- Ventas: 19 consultas sin optimizar y 4 con precarga, para la misma respuesta.
- Evaluaciones: 4 consultas sin optimizar y 1 con select_related, para la misma respuesta.
- Código publicado: c5144bd377d45efcff114b49ab1e0249ed589071.

Las capturas de modelos y HTML corresponden a la copia local combinada, que conserva cambios previos de Semana 7. Las clases de la API son las mismas que las publicadas. El Lab 08 no añade tablas y no publica las modificaciones locales ajenas a este laboratorio.

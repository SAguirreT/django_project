# Laboratorio 10

El documento `GLAB-S10-SAguirreT-RESUELTO.docx` conserva la guía original e incorpora las respuestas de los ejercicios 1–14, justificaciones, capturas de las dos partes y el código completo añadido.

La implementación fue verificada con `npm run lint`, `npm run build` y Chromium/Playwright. Las salidas están en `evidencias/`. Las imágenes `codigo_*`, `estructura_*` y `verificacion_*` son representaciones legibles de los archivos y registros reales; las imágenes de las interacciones fueron capturadas directamente en Chromium.

La investigación propia ya identificada en el Lab 09 corresponde a las siete entidades de FarmaPoint; se reutilizan los componentes en dos listas con estados independientes, conservando exactamente los datos iniciales del proyecto anterior.

Para repetir las pruebas de interfaz: instalar Playwright y Chromium, iniciar Vite en 127.0.0.1:5173 y ejecutar `python lab10/verificar.py`. PLAYWRIGHT_BROWSERS_PATH puede indicar otra instalación de Chromium.

## Estado de publicación

Commit de implementación: `ff90f4b`.

La publicación se completó con la cuenta SAguirreT mediante `git push origin main`. El repositorio remoto incluye el código, las evidencias y el Word con los tres integrantes.

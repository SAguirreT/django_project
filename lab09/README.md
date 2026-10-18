# Laboratorio 09 - FarmaPoint

Integrantes: Dario Maza, Sheila Aguirre y Jose Contreras.

- `Informe_Lab09_FarmaPoint.pdf`: respuestas, justificación y evidencias de los 14 ejercicios.
- `evidencias/`: capturas reales del navegador, código y registros de comandos.
- `capturar.cjs`: pruebas de listas, filtros, vacío, HMR, totales, consola y móvil con Playwright/Edge. Requiere servidor en http://127.0.0.1:5173 y Playwright instalado, o PLAYWRIGHT_PATH apuntando a su paquete. Modifica temporalmente App.jsx y lo restaura con finally; ejecutar sin otros editores modificando el archivo.
- `renderizar_evidencias.cjs`: visor para capturar archivos y registros; no simula una terminal. Recibe la ruta a evidencias/paneles.json.
- `generar_informe.py`: genera el PDF con ReportLab desde las evidencias.

La plantilla oficial inicial y los intentos fallidos se conservan como registro de la preparación. Las comprobaciones finales están en lint.txt, build.txt y pruebas_navegador.json. El generador de capturas escribe imágenes en base64 a stdout para que el proceso que lo invoca las guarde. Las carpetas de caché, revisión visual, dependencias y compilación quedan fuera de Git.

Código de la interfaz: `../frontend/`. La instalación y la demostración están explicadas en su README.

# Laboratorio 08 — Ejercicio 1

## Diagnóstico del proyecto

El repositorio contiene dos árboles Django. `src/core` es una app vacía; para continuar los laboratorios 4–7 corresponde trabajar en `farmacia_project/src`, donde está la app `farmacia`, sus modelos ORM, migraciones, vistas HTML, URLs, templates y registros del Admin. Esos componentes se conservan.

La aplicación contiene diez modelos. Para esta primera parte se reconocen:

- Recurso simple candidato: `Categoria` (también `Proveedor` o `Cliente`, sin relación obligatoria).
- Recurso relacionado candidato: `Producto`, que tiene una ForeignKey `categoria`; también `Venta` se relaciona con `Cliente` y `Producto` mediante `DetalleVenta`.
- Campo de estado existente: `Farmacia.estado` (`CharField`). `EvaluacionUbicacion.nivel_viabilidad` es otro campo categórico que representa el resultado/estado de viabilidad.
- QuerySet personalizado de Semana 7: no se encontró en `farmacia/models.py` ni en el resto de la aplicación; los modelos usan los managers predeterminados. Sí hay QuerySets optimizados con `select_related()`/`prefetch_related()` en vistas, que no son managers personalizados.

`config/settings.py` ya contiene `farmacia` en `INSTALLED_APPS`; DRF se agregó como `rest_framework`. `farmacia/urls.py` y `config/urls.py` mantienen las rutas HTML actuales. Las dependencias discrepaban: `farmacia_project/requirements.txt` decía Django 6.1 mientras la instalación observada, las migraciones y `farmacia_project/src/requirements.txt` usan Django 5.2.17. Se sincronizaron ambos archivos con Django 5.2.17 y Django REST Framework 3.18.3, cuya publicación oficial declara soporte para Django 5.2 y 6.1.

## Cambios del ejercicio 1

- Se registró `rest_framework` en `INSTALLED_APPS`.
- Se incluyó `djangorestframework==3.18.3` en ambos archivos de dependencias del subproyecto.
- No se añadieron serializers, vistas API ni rutas API: corresponden a ejercicios posteriores.
- Se preparó `capturas/ejercicio01/` y la estructura de carpetas de evidencias solicitada.

## Comandos para verificar e instalar

Desde `farmacia_project/src`, con el entorno virtual del proyecto activo:

```powershell
python -m pip install -r requirements.txt
python manage.py check
python -m pip show djangorestframework
```

La instalación aún debe ejecutarse y verificarse en el entorno del usuario; no se da por probada aquí.

## Evidencias que debe tomar el estudiante

- `capturas/ejercicio01/E01_C01_dependencias.png`: VS Code mostrando `src/requirements.txt` con Django y DRF.
- `capturas/ejercicio01/E01_C02_installed_apps.png`: `config/settings.py` mostrando `rest_framework` y `farmacia` dentro de `INSTALLED_APPS`.
- `capturas/ejercicio01/E01_C03_verificacion.png`: terminal con `pip show djangorestframework` y `python manage.py check` ejecutados, mostrando sus resultados reales.
- `capturas/ejercicio01/E01_C04_modelos.png`: `farmacia/models.py` mostrando modelos/relaciones y `Farmacia.estado`; la evidencia debe reflejar que no aparece un manager/queryset personalizado.

## Justificación breve para el informe

Se incorporó Django REST Framework al proyecto existente y se identificaron los modelos y campos que servirán para construir la API. La aplicación HTML, sus URLs, templates y el Admin siguen utilizando los modelos existentes. No se atribuye al repositorio un QuerySet personalizado de Semana 7 porque no se encontró su implementación.

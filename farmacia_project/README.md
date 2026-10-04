# FarmaPoint

## Descripción
FarmaPoint es un sistema web para gestionar y evaluar ubicaciones potenciales para nuevas boticas. Permite registrar zonas, farmacias existentes y evaluaciones de ubicaciones para decidir si una nueva botica sería viable en un determinado punto.

## Problemática
Cuando una cadena de farmacias quiere abrir una nueva sucursal, debe evaluar varios factores: densidad poblacional, flujo de personas, competencia, accesibilidad, presencia de otras farmacias de la misma cadena, centros de salud, costos de alquiler y ventas esperadas. Si estos elementos no se analizan antes, la decisión puede resultar poco rentable o poco viable.

## Objetivo
Ayudar a la toma de decisiones con una evaluación clara y práctica de cada posible ubicación.

## Requisitos funcionales
- RF01: registrar zona con nombre y distrito.
- RF02: registrar densidad poblacional.
- RF03: registrar flujo de personas.
- RF04: registrar accesibilidad.
- RF05: registrar farmacias existentes con tipo.
- RF06: registrar distancia entre farmacia y nueva ubicación.
- RF07: registrar centros de salud cercanos.
- RF08: registrar costo de alquiler.
- RF09: registrar ventas estimadas.
- RF10: calcular viabilidad automáticamente.
- RF11: listar evaluaciones con sus características.
- RF12: comparar ubicaciones para decidir la mejor opción.

## Entidades principales
### Zona
- id
- nombre_zona
- distrito
- densidad_poblacional
- flujo_personas
- accesibilidad

### Farmacia
- id
- nombre
- tipo
- zona_id
- distancia_metros
- estado

### EvaluacionUbicacion
- id
- zona_id
- inkafarmas_cercanos
- competidores_cercanos
- centros_salud_cercanos
- costo_alquiler
- ventas_estimadas
- nivel_viabilidad

## Arquitectura MVT
El proyecto sigue el patrón MVT de Django:

Request -> URL -> View -> Model -> Template -> Response

Los modelos del proyecto están definidos como estructuras en memoria dentro de `farmacia/models.py`. Las vistas consultan esos datos, los formularios validan la información y los templates muestran el resultado.

## Estructura de carpetas
```text
farmacia_project/
├── src/
│   ├── config/
│   ├── farmacia/
│   ├── static/
│   ├── templates/
│   ├── manage.py
│   └── db.sqlite3
├── requirements.txt
├── README.md
└── INSTRUCCIONES_COPILOT.md
```

## Formularios
Se usan formularios `forms.Form` para validar entradas sin ORM ni base de datos:
- `ZonaForm`
- `FarmaciaForm`
- `EvaluacionUbicacionForm`

Incluyen validaciones de campos obligatorios, rangos positivos y valores no negativos.

## Cálculo de viabilidad
La función `calculate_viability` calcula un puntaje considerando:
- densidad poblacional
- flujo de personas
- accesibilidad
- Inkafarmas cercanos
- competidores cercanos
- centros de salud cercanos
- costo de alquiler
- ventas estimadas

La lógica es simple:
- mayor densidad y flujo favorecen la viabilidad
- mayor accesibilidad favorece la viabilidad
- más centros de salud y más competencia disminuyen la puntuación
- alquiler alto baja la puntuación
- mayor ventas estimadas aumentan la puntuación

Después del cálculo:
- 0 a 39 = Baja
- 40 a 69 = Media
- 70 o más = Alta

## Flujo de la aplicación
1. El usuario accede a una URL.
2. Django resuelve la URL en una vista.
3. La vista obtiene o actualiza datos desde `models.py`.
4. La vista carga un template con la información.
5. Django responde con la página HTML construida.

## Cómo ejecutar
```bash
cd farmacia_project/src
python manage.py runserver
```
Luego abre la dirección local indicada por Django, normalmente http://127.0.0.1:8000/

## Sin base de datos
Este proyecto no usa base de datos ni ORM. No se emplean SQLite, PostgreSQL, MySQL ni MongoDB. La información se almacena en listas de diccionarios en memoria dentro de `farmacia/models.py`.

## Datos temporales
Los datos agregados mediante formularios desaparecen al reiniciar el servidor porque se almacenan solo en memoria y no se persisten en una base de datos. Esta decisión cumple la regla del laboratorio y queda documentada aquí.

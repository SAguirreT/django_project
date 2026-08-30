zonas = [
    {
        "id": 1,
        "nombre_zona": "Zona Centro",
        "distrito": "Cercado",
        "densidad_poblacional": 9000,
        "flujo_personas": "Alto",
        "accesibilidad": "Alta",
    },
    {
        "id": 2,
        "nombre_zona": "San Isidro",
        "distrito": "San Miguel",
        "densidad_poblacional": 6200,
        "flujo_personas": "Medio",
        "accesibilidad": "Media",
    },
    {
        "id": 3,
        "nombre_zona": "Las Flores",
        "distrito": "La Victoria",
        "densidad_poblacional": 4100,
        "flujo_personas": "Bajo",
        "accesibilidad": "Baja",
    },
    {
        "id": 4,
        "nombre_zona": "Mercado Norte",
        "distrito": "Breña",
        "densidad_poblacional": 7800,
        "flujo_personas": "Alto",
        "accesibilidad": "Media",
    },
    {
        "id": 5,
        "nombre_zona": "El Dorado",
        "distrito": "Surco",
        "densidad_poblacional": 5300,
        "flujo_personas": "Medio",
        "accesibilidad": "Alta",
    },
]

farmacias = [
    {
        "id": 1,
        "nombre": "Botica San Martín",
        "tipo": "Inkafarma",
        "zona_id": 1,
        "distancia_metros": 180,
        "estado": "Activa",
    },
    {
        "id": 2,
        "nombre": "Farmacia del Sol",
        "tipo": "Competencia",
        "zona_id": 2,
        "distancia_metros": 260,
        "estado": "Activa",
    },
    {
        "id": 3,
        "nombre": "Botica Esperanza",
        "tipo": "Competencia",
        "zona_id": 3,
        "distancia_metros": 420,
        "estado": "Cerrada",
    },
    {
        "id": 4,
        "nombre": "Inkafarma Central",
        "tipo": "Inkafarma",
        "zona_id": 4,
        "distancia_metros": 95,
        "estado": "Activa",
    },
    {
        "id": 5,
        "nombre": "Farmacia La Paz",
        "tipo": "Competencia",
        "zona_id": 5,
        "distancia_metros": 330,
        "estado": "Activa",
    },
]

evaluaciones = [
    {
        "id": 1,
        "zona_id": 1,
        "inkafarmas_cercanos": 1,
        "competidores_cercanos": 1,
        "centros_salud_cercanos": 3,
        "costo_alquiler": 1800,
        "ventas_estimadas": 52000,
        "nivel_viabilidad": "Alta",
    },
    {
        "id": 2,
        "zona_id": 2,
        "inkafarmas_cercanos": 2,
        "competidores_cercanos": 2,
        "centros_salud_cercanos": 2,
        "costo_alquiler": 2400,
        "ventas_estimadas": 38000,
        "nivel_viabilidad": "Media",
    },
    {
        "id": 3,
        "zona_id": 3,
        "inkafarmas_cercanos": 3,
        "competidores_cercanos": 4,
        "centros_salud_cercanos": 1,
        "costo_alquiler": 2900,
        "ventas_estimadas": 22000,
        "nivel_viabilidad": "Baja",
    },
    {
        "id": 4,
        "zona_id": 4,
        "inkafarmas_cercanos": 2,
        "competidores_cercanos": 3,
        "centros_salud_cercanos": 4,
        "costo_alquiler": 2600,
        "ventas_estimadas": 47000,
        "nivel_viabilidad": "Alta",
    },
    {
        "id": 5,
        "zona_id": 5,
        "inkafarmas_cercanos": 1,
        "competidores_cercanos": 2,
        "centros_salud_cercanos": 2,
        "costo_alquiler": 2200,
        "ventas_estimadas": 34000,
        "nivel_viabilidad": "Media",
    },
]


def get_zona_by_id(zona_id):
    for zona in zonas:
        if zona["id"] == zona_id:
            return zona
    return None


def calculate_viability(
    densidad_poblacional,
    flujo_personas,
    accesibilidad,
    inkafarmas_cercanos,
    competidores_cercanos,
    centros_salud_cercanos,
    costo_alquiler,
    ventas_estimadas,
):
    score = 0
    score += densidad_poblacional // 100
    score += {"Alto": 20, "Medio": 10, "Bajo": 0}.get(flujo_personas, 0)
    score += {"Alta": 15, "Media": 10, "Baja": 0}.get(accesibilidad, 0)
    score += centros_salud_cercanos * 6
    score -= competidores_cercanos * 8
    score -= inkafarmas_cercanos * 10
    score += min(ventas_estimadas // 1500, 30)
    score -= max(costo_alquiler // 250, 0)

    if score < 0:
        score = 0

    if 0 <= score <= 39:
        return "Baja"
    if 40 <= score <= 69:
        return "Media"
    return "Alta"

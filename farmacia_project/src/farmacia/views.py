from django.http import Http404
from django.shortcuts import redirect, render

from .forms import EvaluacionUbicacionForm, FarmaciaForm, ZonaForm
from .models import (
    calculate_viability,
    evaluaciones,
    farmacias,
    get_zona_by_id,
    zonas,
)


def inicio(request):
    return render(
        request,
        'farmacia/inicio.html',
        {
            'titulo': 'FarmaPoint',
            'descripcion': 'Sistema para evaluar ubicaciones de nuevas boticas.',
            'objetivo': 'Analizar zonas con base en población, competencia, accesibilidad y rentabilidad.',
        },
    )


def zona_list(request):
    return render(request, 'farmacia/zona_list.html', {'zonas': zonas})


def zona_create(request):
    if request.method == 'POST':
        form = ZonaForm(request.POST)
        if form.is_valid():
            nuevo_id = max((zona['id'] for zona in zonas), default=0) + 1
            zonas.append(
                {
                    'id': nuevo_id,
                    'nombre_zona': form.cleaned_data['nombre_zona'],
                    'distrito': form.cleaned_data['distrito'],
                    'densidad_poblacional': form.cleaned_data['densidad_poblacional'],
                    'flujo_personas': form.cleaned_data['flujo_personas'],
                    'accesibilidad': form.cleaned_data['accesibilidad'],
                }
            )
            return redirect('zona_list')
    else:
        form = ZonaForm()
    return render(request, 'farmacia/zona_form.html', {'form': form, 'titulo': 'Nueva zona'})


def farmacia_list(request):
    return render(request, 'farmacia/farmacia_list.html', {'farmacias': farmacias})


def farmacia_create(request):
    if request.method == 'POST':
        form = FarmaciaForm(request.POST)
        if form.is_valid():
            nuevo_id = max((farmacia['id'] for farmacia in farmacias), default=0) + 1
            farmacias.append(
                {
                    'id': nuevo_id,
                    'nombre': form.cleaned_data['nombre'],
                    'tipo': form.cleaned_data['tipo'],
                    'zona_id': form.cleaned_data['zona_id'],
                    'distancia_metros': form.cleaned_data['distancia_metros'],
                    'estado': form.cleaned_data['estado'],
                }
            )
            return redirect('farmacia_list')
    else:
        form = FarmaciaForm()
    return render(request, 'farmacia/farmacia_form.html', {'form': form, 'titulo': 'Nueva farmacia'})


def evaluacion_list(request):
    items = []
    for evaluacion in evaluaciones:
        zona = get_zona_by_id(evaluacion['zona_id'])
        items.append(
            {
                'id': evaluacion['id'],
                'zona': zona['nombre_zona'] if zona else 'Sin zona',
                'distrito': zona['distrito'] if zona else 'Sin distrito',
                'flujo': zona['flujo_personas'] if zona else '-',
                'accesibilidad': zona['accesibilidad'] if zona else '-',
                'inkafarmas_cercanos': evaluacion['inkafarmas_cercanos'],
                'competidores_cercanos': evaluacion['competidores_cercanos'],
                'centros_salud_cercanos': evaluacion['centros_salud_cercanos'],
                'costo_alquiler': evaluacion['costo_alquiler'],
                'ventas_estimadas': evaluacion['ventas_estimadas'],
                'nivel_viabilidad': evaluacion['nivel_viabilidad'],
            }
        )
    return render(request, 'farmacia/evaluacion_list.html', {'evaluaciones': items})


def evaluacion_create(request):
    if request.method == 'POST':
        form = EvaluacionUbicacionForm(request.POST)
        if form.is_valid():
            zona = get_zona_by_id(form.cleaned_data['zona_id'])
            if zona is None:
                form.add_error('zona_id', 'La zona seleccionada no existe.')
            else:
                nivel = calculate_viability(
                    densidad_poblacional=zona['densidad_poblacional'],
                    flujo_personas=zona['flujo_personas'],
                    accesibilidad=zona['accesibilidad'],
                    inkafarmas_cercanos=form.cleaned_data['inkafarmas_cercanos'],
                    competidores_cercanos=form.cleaned_data['competidores_cercanos'],
                    centros_salud_cercanos=form.cleaned_data['centros_salud_cercanos'],
                    costo_alquiler=float(form.cleaned_data['costo_alquiler']),
                    ventas_estimadas=float(form.cleaned_data['ventas_estimadas']),
                )
                nuevo_id = max((item['id'] for item in evaluaciones), default=0) + 1
                evaluaciones.append(
                    {
                        'id': nuevo_id,
                        'zona_id': zona['id'],
                        'inkafarmas_cercanos': form.cleaned_data['inkafarmas_cercanos'],
                        'competidores_cercanos': form.cleaned_data['competidores_cercanos'],
                        'centros_salud_cercanos': form.cleaned_data['centros_salud_cercanos'],
                        'costo_alquiler': float(form.cleaned_data['costo_alquiler']),
                        'ventas_estimadas': float(form.cleaned_data['ventas_estimadas']),
                        'nivel_viabilidad': nivel,
                    }
                )
                return redirect('evaluacion_list')
    else:
        form = EvaluacionUbicacionForm()
    return render(request, 'farmacia/evaluacion_form.html', {'form': form, 'titulo': 'Nueva evaluación'})


def evaluacion_detail(request, evaluacion_id):
    evaluacion = next((item for item in evaluaciones if item['id'] == evaluacion_id), None)
    if evaluacion is None:
        raise Http404('Evaluación no encontrada.')
    zona = get_zona_by_id(evaluacion['zona_id'])
    return render(
        request,
        'farmacia/evaluacion_detail.html',
        {'evaluacion': evaluacion, 'zona': zona},
    )


def comparacion(request):
    ordenadas = sorted(
        evaluaciones,
        key=lambda item: {'Alta': 3, 'Media': 2, 'Baja': 1}.get(item['nivel_viabilidad'], 0),
        reverse=True,
    )
    mejor = ordenadas[0] if ordenadas else None
    mejor_zona = get_zona_by_id(mejor['zona_id']) if mejor else None
    return render(
        request,
        'farmacia/comparacion.html',
        {'evaluaciones': ordenadas, 'mejor': mejor, 'mejor_zona': mejor_zona},
    )

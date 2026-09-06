from django.http import Http404
from django.shortcuts import redirect, render

from .forms import EvaluacionUbicacionForm, FarmaciaForm, ZonaForm
from .models import Zona, Farmacia, EvaluacionUbicacion


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
    zonas = Zona.objects.all()
    return render(request, 'farmacia/zona_list.html', {'zonas': zonas})


def zona_create(request):
    if request.method == 'POST':
        form = ZonaForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('zona_list')
    else:
        form = ZonaForm()

    return render(
        request,
        'farmacia/zona_form.html',
        {'form': form, 'titulo': 'Nueva zona'}
    )


def farmacia_list(request):
    farmacias = Farmacia.objects.all()
    return render(
        request,
        'farmacia/farmacia_list.html',
        {'farmacias': farmacias}
    )


def farmacia_create(request):
    if request.method == 'POST':
        form = FarmaciaForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('farmacia_list')
    else:
        form = FarmaciaForm()

    return render(
        request,
        'farmacia/farmacia_form.html',
        {'form': form, 'titulo': 'Nueva farmacia'}
    )


def evaluacion_list(request):
    evaluaciones = EvaluacionUbicacion.objects.select_related('zona').all()

    return render(
        request,
        'farmacia/evaluacion_list.html',
        {'evaluaciones': evaluaciones}
    )


def evaluacion_create(request):
    if request.method == 'POST':
        form = EvaluacionUbicacionForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('evaluacion_list')
    else:
        form = EvaluacionUbicacionForm()

    return render(
        request,
        'farmacia/evaluacion_form.html',
        {'form': form, 'titulo': 'Nueva evaluación'}
    )


def evaluacion_detail(request, evaluacion_id):
    try:
        evaluacion = EvaluacionUbicacion.objects.select_related('zona').get(
            id=evaluacion_id
        )
    except EvaluacionUbicacion.DoesNotExist:
        raise Http404('Evaluación no encontrada.')

    return render(
        request,
        'farmacia/evaluacion_detail.html',
        {
            'evaluacion': evaluacion,
            'zona': evaluacion.zona,
        },
    )


def comparacion(request):
    evaluaciones = EvaluacionUbicacion.objects.select_related('zona').all()

    ordenadas = sorted(
        evaluaciones,
        key=lambda item: {
            'Alta': 3,
            'Media': 2,
            'Baja': 1
        }.get(item.nivel_viabilidad, 0),
        reverse=True,
    )

    mejor = ordenadas[0] if ordenadas else None
    mejor_zona = mejor.zona if mejor else None

    return render(
        request,
        'farmacia/comparacion.html',
        {
            'evaluaciones': ordenadas,
            'mejor': mejor,
            'mejor_zona': mejor_zona,
        },
    )
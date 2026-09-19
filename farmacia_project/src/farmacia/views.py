from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    CategoriaForm, ClienteForm, DetalleVentaForm, EvaluacionUbicacionForm,
    FarmaciaForm, PerfilClienteForm, ProductoForm, ProveedorForm, VentaForm, ZonaForm,
)
from .models import (
    Categoria, Cliente, DetalleVenta, EvaluacionUbicacion, Farmacia,
    PerfilCliente, Producto, Proveedor, Venta, Zona,
)

ENTIDADES = {
    'categoria': (Categoria, CategoriaForm, 'Categoría', 'Categorías'),
    'producto': (Producto, ProductoForm, 'Producto', 'Productos'),
    'proveedor': (Proveedor, ProveedorForm, 'Proveedor', 'Proveedores'),
    'cliente': (Cliente, ClienteForm, 'Cliente', 'Clientes'),
    'perfil': (PerfilCliente, PerfilClienteForm, 'Perfil de cliente', 'Perfiles de clientes'),
    'venta': (Venta, VentaForm, 'Venta', 'Ventas'),
}


def inicio(request):
    return render(request, 'farmacia/inicio.html', {
        'titulo': 'FarmaPoint',
        'descripcion': 'Sistema para gestionar una farmacia y evaluar ubicaciones de nuevas boticas.',
        'objetivo': 'Administrar ventas y analizar zonas según población, competencia, accesibilidad y rentabilidad.',
        'categorias': Categoria.objects.count(), 'productos': Producto.objects.count(),
        'proveedores': Proveedor.objects.count(), 'clientes': Cliente.objects.count(),
        'ventas': Venta.objects.count(), 'perfiles': PerfilCliente.objects.count(),
        'detalles': DetalleVenta.objects.count(),
    })


def zona_list(request):
    return render(request, 'farmacia/zona_list.html', {'zonas': Zona.objects.all()})


def zona_create(request):
    form = ZonaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('zona_list')
    return render(request, 'farmacia/zona_form.html', {'form': form, 'titulo': 'Nueva zona'})


def farmacia_list(request):
    return render(request, 'farmacia/farmacia_list.html', {'farmacias': Farmacia.objects.select_related('zona')})


def farmacia_create(request):
    form = FarmaciaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('farmacia_list')
    return render(request, 'farmacia/farmacia_form.html', {'form': form, 'titulo': 'Nueva farmacia'})


def evaluacion_list(request):
    return render(request, 'farmacia/evaluacion_list.html', {'evaluaciones': EvaluacionUbicacion.objects.select_related('zona')})


def evaluacion_create(request):
    form = EvaluacionUbicacionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('evaluacion_list')
    return render(request, 'farmacia/evaluacion_form.html', {'form': form, 'titulo': 'Nueva evaluación'})


def evaluacion_detail(request, evaluacion_id):
    evaluacion = get_object_or_404(EvaluacionUbicacion.objects.select_related('zona'), id=evaluacion_id)
    return render(request, 'farmacia/evaluacion_detail.html', {'evaluacion': evaluacion, 'zona': evaluacion.zona})


def comparacion(request):
    evaluaciones = list(EvaluacionUbicacion.objects.select_related('zona'))
    prioridad = {'Alta': 3, 'Media': 2, 'Baja': 1}
    ordenadas = sorted(evaluaciones, key=lambda item: prioridad.get(item.nivel_viabilidad, 0), reverse=True)
    mejor = ordenadas[0] if ordenadas else None
    return render(request, 'farmacia/comparacion.html', {'evaluaciones': ordenadas, 'mejor': mejor, 'mejor_zona': mejor.zona if mejor else None})


def entidad_list(request, entidad):
    model, _, singular, plural = ENTIDADES[entidad]
    objetos = model.objects.all()
    if entidad == 'producto': objetos = objetos.select_related('categoria')
    elif entidad == 'venta': objetos = objetos.select_related('cliente')
    elif entidad == 'cliente': objetos = objetos.select_related('perfil').prefetch_related('ventas')
    elif entidad == 'categoria': objetos = objetos.prefetch_related('productos')
    elif entidad == 'perfil': objetos = objetos.select_related('cliente')
    return render(request, 'farmacia/entidad_list.html', {'objetos': objetos, 'entidad': entidad, 'singular': singular, 'plural': plural})


def entidad_create(request, entidad):
    _, form_class, singular, _ = ENTIDADES[entidad]
    initial = {'fecha': timezone.localtime().strftime('%Y-%m-%dT%H:%M')} if entidad == 'venta' and request.method == 'GET' else None
    form = form_class(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('entidad_list', entidad=entidad)
    return render(request, 'farmacia/entidad_form.html', {'form': form, 'entidad': entidad, 'singular': singular, 'accion': 'Registrar'})


def entidad_update(request, entidad, pk):
    model, form_class, singular, _ = ENTIDADES[entidad]
    objeto = get_object_or_404(model, pk=pk)
    form = form_class(request.POST or None, instance=objeto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('entidad_list', entidad=entidad)
    return render(request, 'farmacia/entidad_form.html', {'form': form, 'entidad': entidad, 'singular': singular, 'accion': 'Editar', 'objeto': objeto})


def entidad_delete(request, entidad, pk):
    model, _, singular, _ = ENTIDADES[entidad]
    objeto = get_object_or_404(model, pk=pk)
    if request.method == 'POST':
        objeto.delete()
        return redirect('entidad_list', entidad=entidad)
    return render(request, 'farmacia/entidad_confirm_delete.html', {'objeto': objeto, 'entidad': entidad, 'singular': singular})


def venta_detail(request, pk):
    venta = get_object_or_404(Venta.objects.select_related('cliente').prefetch_related('detalles__producto'), pk=pk)
    return render(request, 'farmacia/venta_detail.html', {'venta': venta})


def detalleventa_list(request):
    return render(request, 'farmacia/detalleventa_list.html', {'detalles': DetalleVenta.objects.select_related('venta__cliente', 'producto')})


def detalleventa_create(request):
    form = DetalleVentaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('detalleventa_list')
    return render(request, 'farmacia/detalleventa_form.html', {'form': form, 'accion': 'Registrar'})


def detalleventa_update(request, pk):
    detalle = get_object_or_404(DetalleVenta, pk=pk)
    form = DetalleVentaForm(request.POST or None, instance=detalle)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('detalleventa_list')
    return render(request, 'farmacia/detalleventa_form.html', {'form': form, 'accion': 'Editar', 'detalle': detalle})


def detalleventa_delete(request, pk):
    detalle = get_object_or_404(DetalleVenta, pk=pk)
    if request.method == 'POST':
        detalle.delete()
        return redirect('detalleventa_list')
    return render(request, 'farmacia/detalleventa_confirm_delete.html', {'detalle': detalle})

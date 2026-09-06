from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CategoriaForm, ClienteForm, ProductoForm, ProveedorForm, VentaForm
from .models import Categoria, Cliente, Producto, Proveedor, Venta

ENTIDADES = {
    'categoria': (Categoria, CategoriaForm, 'Categoría', 'Categorías'),
    'producto': (Producto, ProductoForm, 'Producto', 'Productos'),
    'proveedor': (Proveedor, ProveedorForm, 'Proveedor', 'Proveedores'),
    'cliente': (Cliente, ClienteForm, 'Cliente', 'Clientes'),
    'venta': (Venta, VentaForm, 'Venta', 'Ventas'),
}


def inicio(request):
    return render(request, 'farmacia/inicio.html', {
        'categorias': Categoria.objects.count(), 'productos': Producto.objects.count(),
        'proveedores': Proveedor.objects.count(), 'clientes': Cliente.objects.count(), 'ventas': Venta.objects.count(),
    })


def entidad_list(request, entidad):
    model, _, singular, plural = ENTIDADES[entidad]
    objetos = model.objects.all()
    if entidad in ('producto', 'venta'):
        objetos = objetos.select_related('categoria' if entidad == 'producto' else 'cliente')
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

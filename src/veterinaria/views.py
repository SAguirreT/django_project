from django.shortcuts import render, redirect, get_object_or_404
from .models import Propietario


def inicio(request):
    return render(request, 'veterinaria/inicio.html')


# LISTAR PROPIETARIOS
def listar_propietarios(request):
    propietarios = Propietario.objects.all()

    return render(
        request,
        'veterinaria/propietarios.html',
        {'propietarios': propietarios}
    )


# CREAR PROPIETARIO
def crear_propietario(request):

    if request.method == 'POST':

        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')

        Propietario.objects.create(
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            correo=correo
        )

        return redirect('listar_propietarios')

    return render(
        request,
        'veterinaria/propietario_form.html'
    )


# EDITAR PROPIETARIO
def actualizar_propietario(request, id):

    propietario = get_object_or_404(
        Propietario,
        id=id
    )

    if request.method == 'POST':

        propietario.nombre = request.POST.get('nombre')
        propietario.apellido = request.POST.get('apellido')
        propietario.telefono = request.POST.get('telefono')
        propietario.correo = request.POST.get('correo')

        propietario.save()

        return redirect('listar_propietarios')

    return render(
        request,
        'veterinaria/propietario_form.html',
        {'propietario': propietario}
    )


# ELIMINAR PROPIETARIO
def eliminar_propietario(request, id):

    propietario = get_object_or_404(
        Propietario,
        id=id
    )

    if request.method == 'POST':
        propietario.delete()
        return redirect('listar_propietarios')

    return render(
        request,
        'veterinaria/confirmar_eliminacion.html',
        {'propietario': propietario}
    )
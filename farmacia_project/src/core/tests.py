from django.shortcuts import render
from django.http import HttpResponse

def inicio_farmacia(request):
    return HttpResponse("<h1>¡Felicidades! Tu sistema de Farmacia está funcionando.</h1>")
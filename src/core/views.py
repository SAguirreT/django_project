from django.shortcuts import render
from django.http import HttpResponse

# Esta es tu primera vista
def inicio_farmacia(request):
    # Por ahora devolveremos un mensaje de texto. 
    # Más adelante aquí pondrás: return render(request, 'tu_archivo.html')
    return HttpResponse("<h1>¡Felicidades! Tu sistema de Farmacia está funcionando.</h1>") 
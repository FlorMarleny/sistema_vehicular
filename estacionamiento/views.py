from django.shortcuts import render


def estacionamiento_view(request):
    return render(request, 'estacionamiento.html')

from django.shortcuts import render
from .models import Producto

def lista_productos(request):
    productos = Producto.objects.all()  # Trae todos los productos
    return render(request, 'productos/lista.html', {'productos': productos})
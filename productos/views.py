from django.shortcuts import render
from .models import Producto
from django.db.models import Q

def lista_productos(request):
    productos = Producto.objects.all()

    q = request.GET.get('q', '').strip()
    categoria = request.GET.get('type', '').strip()
    marca = request.GET.get('brand', '').strip()
    precio_min = request.GET.get('min', '').strip()
    precio_max = request.GET.get('max', '').strip()
    nuevo = request.GET.get('nuevo')
    usado = request.GET.get('usado')
    sort = request.GET.get('sort', '')

    if q:
        productos = productos.filter(
            Q(nombre__icontains=q) |
            Q(descripcion__icontains=q)
        )

    if categoria:
        productos = productos.filter(categoria__iexact=categoria)

    if marca:
        try:
            productos = productos.filter(marca__nombre__iexact=marca)
        except Exception:
            productos = productos.filter(marca__iexact=marca)

    try:
        if precio_min != '':
            productos = productos.filter(precio__gte=float(precio_min))
    except ValueError:
        pass

    try:
        if precio_max != '':
            productos = productos.filter(precio__lte=float(precio_max))
    except ValueError:
        pass

    if nuevo and not usado:
        productos = productos.filter(estado__iexact='nuevo')
    if usado and not nuevo:
        productos = productos.filter(estado__iexact='usado')

    if sort == 'priceAsc':
        productos = productos.order_by('precio')
    elif sort == 'priceDesc':
        productos = productos.order_by('-precio')
    elif sort == 'rating':
        productos = productos.order_by('-valoracion')
    else:
        productos = productos.order_by('-id')

    return render(request, 'productos/lista.html', {
        'productos': productos,
        'request': request,
    })
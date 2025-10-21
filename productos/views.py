from django.shortcuts import render
from .models import Producto, CarouselImage

def lista_productos(request):
    """
    Vista principal para mostrar los productos y el carrusel en la página de inicio.
    """
    productos = Producto.objects.all()

    q = request.GET.get('q', '')
    tipo = request.GET.get('type', '')
    marca = request.GET.get('brand', '')
    min_precio = request.GET.get('min', '')
    max_precio = request.GET.get('max', '')
    nuevo = request.GET.get('nuevo')
    usado = request.GET.get('usado')
    sort = request.GET.get('sort', '')

    if q:
        productos = productos.filter(nombre__icontains=q) | productos.filter(descripcion__icontains=q)

    if tipo:
        productos = productos.filter(categoria__iexact=tipo)

    if marca:
        productos = productos.filter(marca__iexact=marca)

    if min_precio:
        try:
            productos = productos.filter(precio__gte=float(min_precio))
        except ValueError:
            pass

    if max_precio:
        try:
            productos = productos.filter(precio__lte=float(max_precio))
        except ValueError:
            pass

    if nuevo and not usado:
        productos = productos.filter(estado__iexact='nuevo')
    elif usado and not nuevo:
        productos = productos.filter(estado__iexact='usado')

    if sort == 'priceAsc':
        productos = productos.order_by('precio')
    elif sort == 'priceDesc':
        productos = productos.order_by('-precio')
    elif sort == 'rating':
        productos = productos.order_by('-valoracion')
    else:
        productos = productos.order_by('-id')

    carousel_images = CarouselImage.objects.all()

    context = {
        'productos': productos,
        'carousel_images': carousel_images
    }

    return render(request, 'productos/lista.html', context)
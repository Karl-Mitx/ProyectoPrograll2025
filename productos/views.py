from django.shortcuts import render
from .models import Producto, CarouselImage, PromoCard
from django.db.models import Q

def lista_productos(request):
 
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
    promo_cards = PromoCard.objects.filter(activo=True).order_by('orden')[:6]

    context = {
        'productos': productos,
        'carousel_images': carousel_images,
        'promo_cards': promo_cards,
    }
    return render(request, 'productos/lista.html', context)

def productos_todos(request):
    """
    Página 'Ver todos': sidebar + grilla/lista, con búsqueda, marca y orden.
    """
    productos = Producto.objects.all()
    
    q = request.GET.get('q', '').strip()
    brand = request.GET.get('brand', '').strip()
    sort = request.GET.get('sort', 'relevance')

    if q:
        productos = productos.filter(
            Q(nombre__icontains=q) |
            Q(descripcion__icontains=q) |
            Q(categoria__icontains=q) |
            Q(marca__icontains=q)
        )

    if brand:
        productos = productos.filter(marca__iexact=brand)


    if sort == 'priceAsc':
        productos = productos.order_by('precio')
    elif sort == 'priceDesc':
        productos = productos.order_by('-precio')
    elif sort == 'name':
        productos = productos.order_by('nombre')
    else:
        productos = productos.order_by('-id')

    brands = (Producto.objects
              .order_by('marca')
              .values_list('marca', flat=True)
              .distinct())

    context = {
        'productos': productos,
        'q': q,
        'brand': brand,
        'sort': sort,
        'brands': brands,
    }
    return render(request, 'productos/todos.html', context)

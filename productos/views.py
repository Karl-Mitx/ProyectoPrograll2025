from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Producto, CarouselImage, PromoCard, PromoPill, Profile, Pedido
from .forms import PedidoForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

#aqui van las vistas de los pedidos
@login_required
def crear_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.cliente = request.user
            pedido.save()
            return redirect('pedido_confirmado')  
    else:
        form = PedidoForm()
    return render(request, 'pedidos/crear_pedido.html', {'form': form})
@login_required
def pedido_confirmado(request):
    pedidos=Pedido.objects.filter(cliente=request.user).order_by('-fecha')
    ultimo_pedido = pedidos.first()
    if ultimo_pedido:
        precio=float(ultimo_pedido.producto.precio)
        cantidad=int(ultimo_pedido.cantidad)
        subtotal=precio*cantidad
        iva=subtotal*0.12
        total=subtotal+iva
    else:
        subtotal=0
        iva=0
        total=0
    return render(request, 'pedidos/pedido_confirmado.html', {'pedido': ultimo_pedido, 'subtotal': subtotal, 'iva': iva, 'total': total})   


def lista_productos(request):
    productos = Producto.objects.all()

    q          = request.GET.get('q', '').strip()
    tipo       = request.GET.get('type', '').strip()
    marca      = request.GET.get('brand', '').strip()
    min_precio = request.GET.get('min', '').strip()
    max_precio = request.GET.get('max', '').strip()
    nuevo      = request.GET.get('nuevo')
    usado      = request.GET.get('usado')
    sort       = request.GET.get('sort', '')

    if q:
        productos = productos.filter(
            Q(nombre__icontains=q) | Q(descripcion__icontains=q)
        )

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
        productos = productos.order_by('-id')
    else:
        productos = productos.order_by('-id')
        
    gamer_products = (Producto.objects
                    .filter(categoria__in=['Consola', 'Videojuego', 'Gaming'])
                    .order_by('-id')[:12])

    carousel_images = CarouselImage.objects.all()
    promo_cards     = PromoCard.objects.filter(activo=True).order_by('orden')[:6]
    promo_pills     = PromoPill.objects.filter(activo=True).order_by('orden')[:2]

    context = {
        'productos': productos,
        'carousel_images': carousel_images,
        'promo_cards': promo_cards,
        'promo_pills': promo_pills,
        'gamer_products': gamer_products,
    }
    return render(request, 'productos/lista.html', context)


def productos_todos(request):
    productos = Producto.objects.all()

    q     = request.GET.get('q', '').strip()
    brand = request.GET.get('brand', '').strip()
    sort  = request.GET.get('sort', 'relevance')

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

    brands = (Producto.objects.order_by('marca')
            .values_list('marca', flat=True).distinct())

    return render(request, 'productos/todos.html', {
        'productos': productos,
        'q': q, 'brand': brand, 'sort': sort, 'brands': brands,
    })

@login_required
def toggle_favorito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    profile = Profile.objects.get(user=request.user)

    if producto in profile.favoritos.all():
        profile.favoritos.remove(producto)
    else:
        profile.favoritos.add(producto)

    return redirect(request.META.get('HTTP_REFERER', 'lista_productos'))

@login_required
def favoritos_lista(request):
    """Muestra la lista de productos favoritos del usuario."""
    favoritos = request.user.profile.favoritos.all()  # asumiendo que tu modelo Profile tiene un ManyToManyField a Producto
    return render(request, 'productos/favoritos.html', {'favoritos': favoritos})

@login_required
def toggle_favorito(request, producto_id):
    """Agrega o quita un producto de favoritos (AJAX)."""
    producto = Producto.objects.get(id=producto_id)
    profile = request.user.profile

    if producto in profile.favoritos.all():
        profile.favoritos.remove(producto)
        estado = 'removed'
    else:
        profile.favoritos.add(producto)
        estado = 'added'

        return redirect(request.META.get('HTTP_REFERER', 'productos'))
    return redirect(request.META.get('HTTP_REFERER', 'productos'))

@csrf_exempt
@login_required
def crear_pedido_desde_carrito(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            items = data.get('items', [])
            tipo_pago = data.get('tipo_pago', 'tarjeta')
            
            for item in items:
                producto_id = item.get('id')
                cantidad = item.get('qty', 1)
                producto = Producto.objects.get(id=producto_id)
                
                Pedido.objects.create(
                    cliente=request.user,
                    producto=producto,
                    cantidad=cantidad,
                    tipo_pago=tipo_pago  
                )
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def confirmar_datos_cliente(request):
    if request.method == 'POST':
        form = DatosClienteForm(request.POST)
        if form.is_valid():
            datos = form.save(commit=False)
            datos.usuario = request.user
            datos.save()
            return redirect('pedido_confirmado')
    else:
        form = DatosClienteForm(initial={'tipo_pago': 'tarjeta'})

    return render(request, 'pedidos/confirmar_datos_cliente.html', {'form': form})

from django.contrib import admin
from .models import Producto
from .models import CarouselImage

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'marca', 'precio', 'estado')
    list_filter = ('estado', 'categoria', 'marca')
    
@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'activo', 'orden')
    list_editable = ('activo', 'orden')
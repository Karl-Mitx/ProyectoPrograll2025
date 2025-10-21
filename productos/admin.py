from django.contrib import admin
from .models import Producto
from .models import CarouselImage
from .models import PromoCard
from .models import PromoPill

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'marca', 'precio', 'estado')
    list_filter = ('estado', 'categoria', 'marca')
    
@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'activo', 'orden')
    list_editable = ('activo', 'orden')
    
@admin.register(PromoCard)
class PromoCardAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'activo', 'orden')
    list_editable = ('activo', 'orden')
    search_fields = ('titulo', 'badge_text')

@admin.register(PromoPill)
class PromoPillAdmin(admin.ModelAdmin):
    list_display = ('label_html', 'variante', 'activo', 'orden')
    list_editable = ('variante', 'activo', 'orden')
    search_fields = ('label_html', 'cta_text')
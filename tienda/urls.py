from django.contrib import admin
from django.urls import path, include  # <--- include agregado

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('productos.urls')),  # todas las URLs de productos
]
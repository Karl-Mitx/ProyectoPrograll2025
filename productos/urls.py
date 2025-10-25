from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import crear_pedido, crear_pedido_desde_carrito, pedido_confirmado

from . import views
from . import views_accounts

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('productos/todos/', views.productos_todos, name='productos_todos'),
    path('productos/<int:producto_id>/favorito/', views.toggle_favorito, name='toggle_favorito'),

    path('accounts/login/',  auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='lista_productos'),       name='logout'),
    path('accounts/signup/', views_accounts.signup,   name='signup'),
    path('accounts/profile/', views_accounts.profile, name='profile'),
    path('productos/<int:producto_id>/toggle_favorito/', views.toggle_favorito, name='toggle_favorito'),
    path('favoritos/', views.favoritos_lista, name='favoritos_lista'),
    path('favoritos/toggle/<int:producto_id>/', views.toggle_favorito, name='toggle_favorito'),
    path('pedido/nuevo/', crear_pedido, name='crear_pedido'),
    path('pedido/crear-desde-carrito/', crear_pedido_desde_carrito, name='crear_pedido_desde_carrito'),
    path('pedido/confirmado/', pedido_confirmado, name='pedido_confirmado'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
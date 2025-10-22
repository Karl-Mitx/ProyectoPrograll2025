from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import views
from . import views_accounts

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('productos/todos/', views.productos_todos, name='productos_todos'),

    path('accounts/login/',  auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='lista_productos'),       name='logout'),
    path('accounts/signup/', views_accounts.signup,   name='signup'),
    path('accounts/profile/', views_accounts.profile, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
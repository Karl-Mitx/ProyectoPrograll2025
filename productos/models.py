from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from urllib.parse import urlencode


def avatar_upload_to(instance, filename):
    return f"avatars/user_{instance.user_id}/{filename}"

TIPO_PAGO_CHOICES = [
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia bancaria'),
        ('efectivo', 'Pago contra entrega'),
    ]
class Pedido(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos', null=True)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    tipo_pago = models.CharField(max_length=20, choices=TIPO_PAGO_CHOICES)
    fecha = models.DateTimeField(auto_now_add=True)
    enviado = models.BooleanField(default=False)
    recibido = models.BooleanField(default=False)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.username}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to=avatar_upload_to, blank=True, null=True)
    favoritos = models.ManyToManyField('Producto', blank=True, related_name='favorito_por')

    def __str__(self):
        return f"Perfil de {self.user.username}"


@receiver(post_save, sender=User)
def ensure_profile(sender, instance, created, **kwargs):
    Profile.objects.get_or_create(user=instance)


class Producto(models.Model):
    CATEGORIAS = [
        ('Computadora', 'Computadora'),
        ('Laptop', 'Laptop'),
        ('Smartphone', 'Smartphone'),
        ('Tablet', 'Tablet'),
        ('Audifonos', 'Audífonos'),
        ('TV', 'Televisor'),
        ('Consola', 'Consola'),
        ('Videojuego', 'Videojuego'),
        ('Accesorio', 'Accesorio'),
        ('Microcontrolador', 'Microcontrolador'),
        ('Impresora', 'Impresora'),
        ('Cámara', 'Cámara'),
        ('Dron', 'Dron'),
        ('Electrodoméstico', 'Electrodoméstico'),
        ('Redes', 'Redes y Conectividad'),
        ('Almacenamiento', 'Almacenamiento'),
        ('Monitores', 'Monitores'),
        ('Componentes', 'Componentes de PC'),
        ('Smartwatch', 'Smartwatch / Wearables'),
        ('Audio', 'Audio y Sonido'),
        ('Proyector', 'Proyector'),
        ('Software', 'Software'),
        ('Energía', 'Energía / UPS / Baterías'),
        ('IoT', 'Internet de las Cosas (IoT)'),
        ('Domótica', 'Domótica'),
        ('Electrónica', 'Electrónica General'),
        ('Gaming', 'Gaming'),
        ('Cables', 'Cables y Adaptadores'),
        ('Cocina', 'Cocina Inteligente'),
        ('Oficina', 'Oficina y Periféricos'),
        ('Iluminación', 'Iluminación LED / Smart'),
    ]

    MARCAS = [
        ('Samsung', 'Samsung'),
        ('LG', 'LG'),
        ('HP', 'HP'),
        ('Whirlpool', 'Whirlpool'),
        ('Xiaomi', 'Xiaomi'),
        ('Frigidaire', 'Frigidaire'),
        ('Mabe', 'Mabe'),
        ('Hisense', 'Hisense'),
        ('Apple', 'Apple'),
        ('Sony', 'Sony'),
        ('DELL', 'DELL'),
        ('Black+Decker', 'Black+Decker'),
        ('Motorola', 'Motorola'),
        ('Lenovo', 'Lenovo'),
        ('Honor', 'Honor'),
        ('Huawei', 'Huawei'),
        ('Nintendo', 'Nintendo'),
        ('Oster', 'Oster'),
        ('JBL', 'JBL'),
        ('KitchenAid', 'KitchenAid'),
        ('Toshiba', 'Toshiba'),
        ('Remington', 'Remington'),
        ('DJI', 'DJI'),
        ('Acer', 'Acer'),
        ('Panasonic', 'Panasonic'),
        ('Skullcandy', 'Skullcandy'),
        ('Garmin', 'Garmin'),
        ('Epson', 'Epson'),
        ('General Electric', 'General Electric'),
        ('Canon', 'Canon'),
        ('Microsoft', 'Microsoft'),
        ('Panamax', 'Panamax'),
        ('EnergyMax', 'EnergyMax'),
        ('Barkan', 'Barkan'),
        ('Aiwa', 'Aiwa'),
        ('iRobot', 'iRobot'),
        ('Taurus', 'Taurus'),
        ('Razer', 'Razer'),
        ('Logitech', 'Logitech'),
        ('Segway', 'Segway'),
        ('Cuisinart', 'Cuisinart'),
        ('Homedics', 'Homedics'),
        ('Karcher', 'Karcher'),
        ('APC', 'APC'),
        ('Zagg', 'Zagg'),
        ('Revlon', 'Revlon'),
        ('Klip Xtreme', 'Klip Xtreme'),
        ('Solo', 'Solo'),
        ('Forza', 'Forza'),
        ('Klip', 'Klip'),
        ('Midland', 'Midland'),
        ('Marshall', 'Marshall'),
        ('Tucano', 'Tucano'),
        ('Soportv', 'Soportv'),
        ('Xtech', 'Xtech'),
        ('Fitbit', 'Fitbit'),
        ('Salicru', 'Salicru'),
        ('Drinkmate', 'Drinkmate'),
        ('Thule', 'Thule'),
        ('Steren', 'Steren'),
        ('Navia', 'Navia'),
        ('George Foreman', 'George Foreman'),
        ('Nescafe Dolce Gusto', 'Nescafe Dolce Gusto'),
        ('KIDdesigns', 'KIDdesigns'),
        ('Delonghi', 'Delonghi'),
        ('Eset', 'Eset'),
        ('Holstein', 'Holstein'),
        ('Mybat', 'Mybat'),
        ('Wahl', 'Wahl'),
        ('Niu', 'Niu'),
        ('Casio', 'Casio'),
        ('Philips', 'Philips'),
        ('Wacom', 'Wacom'),
        ('Adam Elements', 'Adam Elements'),
        ('RCA', 'RCA'),
        ('Popsockets', 'Popsockets'),
        ('TP-LINK', 'TP-LINK'),
        ('Sandisk', 'Sandisk'),
        ('Vivitar', 'Vivitar'),
        ('Mr Coffee', 'Mr Coffee'),
        ('Dyson', 'Dyson'),
        ('Starlink', 'Starlink'),
        ('Totto', 'Totto'),
        ('ISDIN', 'ISDIN'),
        ('Brumate', 'Brumate'),
        ('Tocobo', 'Tocobo'),
        ('Skin 1004', 'Skin 1004'),
        ('Shark', 'Shark'),
        ('Bonefly', 'Bonefly'),
        ('Tec Italy', 'Tec Italy'),
        ('Tía Mía', 'Tía Mía'),
        ('Targus', 'Targus'),
        ('Ninja', 'Ninja'),
    ]

    ESTADOS = [
        ('nuevo', 'Nuevo'),
        ('usado', 'Usado'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, blank=True)
    marca = models.CharField(max_length=20, choices=MARCAS, blank=True)
    estado = models.CharField(max_length=5, choices=ESTADOS, default='nuevo')
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre


class CarouselImage(models.Model):
    titulo = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='carousel/')
    enlace = models.URLField(blank=True, help_text="URL al que redirige al hacer click, opcional")
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return self.titulo or f"Imagen {self.id}"


class PromoCard(models.Model):
    BADGE_STYLES = [
        ('solid', 'Sólido'),
        ('ghost', 'Ghost (borde claro)'),
    ]

    titulo = models.CharField(max_length=120)
    badge_text = models.CharField(max_length=40, blank=True)
    badge_style = models.CharField(max_length=10, choices=BADGE_STYLES, default='solid')
    cta_text = models.CharField(max_length=40, default='Ver ofertas')
    enlace = models.URLField(blank=True)
    imagen = models.ImageField(upload_to='promos/', blank=True, null=True)

    gradiente_clase = models.CharField(
        max_length=20,
        blank=True,
        help_text="Ej: house, tennis, starlink, scooter, baby, kitchen"
    )

    texto_claro = models.BooleanField(
        default=False,
        help_text="Marcar si el texto debe ir claro (para fondos oscuros)."
    )
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return self.titulo


class PromoPill(models.Model):
    VARIANTES = [
        ('default', 'Default'),
        ('soft', 'Soft'),
    ]

    label_html = models.CharField(max_length=180)
    cta_text = models.CharField(max_length=40, default='Ver más')
    enlace = models.URLField(blank=True)
    variante = models.CharField(max_length=10, choices=VARIANTES, default='default')

    filtro_q = models.CharField(max_length=120, blank=True)
    filtro_brand = models.CharField(max_length=40, blank=True)

    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"Pill: {self.label_html[:40]}"

    def get_url(self):
        if self.enlace:
            return self.enlace
        params = {}
        if self.filtro_q:
            params['q'] = self.filtro_q
        if self.filtro_brand:
            params['brand'] = self.filtro_brand
        base = reverse('productos_todos')
        return f"{base}?{urlencode(params)}" if params else base
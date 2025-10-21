from django.db import models

class Producto(models.Model):
    CATEGORIAS = [
        ('Computadora', 'Computadora'),
        ('Smartphone', 'Smartphone'),
        ('Audifonos', 'Audífonos'),
        ('TV', 'TV'),
        ('Consola', 'Consola'),
        ('Accesorio', 'Accesorio'),
        ('Microcontrolador', 'Microcontrolador'),
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
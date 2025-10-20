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
        ('Apple', 'Apple'),
        ('Samsung', 'Samsung'),
        ('Sony', 'Sony'),
        ('Logitech', 'Logitech'),
        ('Xiaomi', 'Xiaomi'),
        ('Arduino', 'Arduino'),
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
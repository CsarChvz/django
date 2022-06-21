import email
from filecmp import DEFAULT_IGNORES
from itertools import product
from mmap import PROT_EXEC
from pyexpat import model
from django.db import models

# Create your models here.

## Relacion ManyToMany

#       -- Esta clase va aestar a si:
#       "Una promocion puede tener varios productos y un producto puede estar en varias promociones"
class Promotion(models.Model):
    descrption = models.CharField(max_length=255)
    discount = models.FloatField()
    # product_set


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey("Product", on_delete=models.SET_NULL, null=True, related_name="+")

class Product(models.Model):
    #sku = models.CharField(max_length=10, primary_key=True)
    title = models.CharField(max_length=255) #varchar(255)
    slug = models.SlugField()
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2) # Siempre usar
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    # En el parametro on.delete se pone PROTECT por si accidentalmente se termina borrando un colleción
    # entonces para que no se terminen de borrar los productos que tienen esa collection
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)


class Customer(models.Model):
    #Huma readable name estos van a ser usados para elegir los campos
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = "S"
    MEMBERSHIP_GOLD = "G"

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    first_name = models.CharField(max_length=255)
    
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    # Campos de eleccion y posibles valores en el campo y su valor default
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)


    # Se agrega una subclase la cual va a tener los metados de nuestra tabla
    class Meta:
        db_table = "store_customers"
        # ¿Para que se usan los index?

        # -- Se usan para acelerar nuestras busquedas de la base de datos
        indexes = [
            models.Index(fields=["last_name", "first_name"])
        ]


class Order(models.Model):

    # Elecciones de status
    STATUS_PENDING = "P"
    STATUS_COMPLETE = "C"
    STATUS_FAILED = "F"
    #Choices
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_COMPLETE, "Complete"),
        (STATUS_FAILED, "Failed"),
    ]
    # La primera vez que agreguemos una orden se va agregar la hora
    placed_at = models.DateField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


# --- RELACIONES ENTRE ENTIDADES ---------

#   // La entidad padre deberá existir antes de que creamos la entidad hija
#       // Entonces en la entidad hija debemos especificar la entidad padre
#       // No se tiene que definir en la entidad padre ya que DJANGO lo hace automaticamente
#   // AQUI SIGUIENTE EJEMPLO
#   ___ Relación OneToOne

### Este es un ejemplo de OneToOne
# class Address(models.Model):
#     street = models.CharField(max_length=255)
#     city = models.CharField(max_length=255)
#     customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)

### Podemos asumir que el "customer" pueda tener varias direcciones, entonces tenemos que cambiar el modelo de la 
#       la entidad anterior y cambiar su tipo de relacion con la entidad padre

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    # Tenemos que cambiar el tipo de dato como Fo
    # reignKey para las relaciones
    zip_code = models.IntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
from django.shortcuts import render
from django.http import HttpResponse

from store.models import Collection, Order, Product, Customer
# Create your views here.
def say_hello(request):
    #query_set = Product.objects.all()

    # En djgango para buscar los productos que son mayor o con nua condicion, no se usan los operadores > <
    # Si no su forma es keyword = value
    # Entonces para hacerlo se pone el nombre del la keyword y dos guiones bajos, despues la condicion
    # Estas condiciones son:
    # gt = "grater than"
    # gte = "grater than or equal"
    # lt = "less than"
    # lte = "less than or equal"

    #Quedaría así una condicion

    # unit_price__gt=20
    # keyword__[condicionDjango]=value 

    #Estos se llaman Fields lookups
    #https://docs.djangoproject.com/en/4.0/ref/models/querysets/#field-lookups
    #query_set = Product.objects.filter(unit_price__gt=20)

    #Para rango seria algo igual pero el value seria una tupla
    #query_set = Product.objects.filter(unit_price__range=(20, 30))

    # Para checar si contienen algo se pueden con 
    # keyword__icontains
    #query_set = Product.objects.filter(title__icontains="coffee")


    # Ejercicios
    # --- Customers with .com accounts ---
    #com_accounts = Customer.objects.filter(email__contains=".com")
    # --- Collections that don’t have a featured product ---
    # collections = Collection.objects.filter(featured_product__isnull=True)
    # --- Products with low inventory (less than 10) ---
    # productos = Product.objects.filter(inventory__lt=10)
    # --- Orders placed by customer with id = 1 ---
    query_set = Order.objects.filter(customer__id=1)
    return render(request, "hello.html",{'name': 'Mosh', 'products': list(query_set)})


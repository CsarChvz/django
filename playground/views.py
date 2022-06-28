from ast import Or
from itertools import product
from django.shortcuts import render
from django.http import HttpResponse
from store.models import Collection, Order, OrderItem, Product, Customer
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
def say_hello(request):

    # Agregacion de objetos

    # A veces queremos computar operaciones y por eso se usa el metodo "aggregate" en la clase de la instancia
    # El metodo aggregate no retornar un "query_set" sino un diccionario con el valor

    # Este cuenta el numero de productos
    Product.objects.aggregate(Count('id'))
    # Pero si ponemos otro campo, este va a detectar o contar los campos que tengan una descripción
    Product.objects.aggregate(Count('description'))

    result = Product.objects.aggregate(Count('id'))

    # Tambien con las clases que importamos, podemos calcular varias cosas
    # Adentro de la clase se va a pasar el nombre del campo que queremos encontrar el Minimo
    result = Product.objects.aggregate(Count('id'), min_price=Min('unit_price'))

    # También podemos filtrar
    result = Product.objects.filter(collection__id=1).aggregate(Count('id'), min_price=Min('unit_price'))

    #Ejercicios
    #How many orders do we have?
    result = Order.objects.aggregate(count_order=Count(id))

    #How many units of product 1 have we sold?
    result =  OrderItem.objects.filter(product__id=1).aggregate(units_sold=Sum("quantity"))

    #How many units of product 1 have we sold?
    result =  OrderItem.objects.filter(product__id=1).aggregate(count=Count("id"))

    #How many orders has customer 1 placed?
    result = Order.objects.filter(customer__id=1).aggregate(count_customer=Count("id"))
    
    #What is the min, max and average price of the products in collection 3?
    result = Product.objects.filter(collection__id=3).aggregate(min=Min("unit_price"), max=Max("unit_price"), average=Avg("unit_price"))

    return render(request, "hello.html",{'name': 'Mosh', 'result': result})

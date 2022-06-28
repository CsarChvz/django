from django.shortcuts import render
from django.http import HttpResponse

from store.models import Collection, Order, OrderItem, Product, Customer
# Create your views here.
def say_hello(request):
    # Deferring Fields ----
    # Este metodo only a diferencia del metodo values, no devuelve un diccionario

    # Hay que tener cuidado  cuando se usa el only, ya que vamos a terminar con varias consultas
    #query_set = Product.objects.only('id', 'title')

    # Existe otro metodo diferente al values el cual se llama "defer"
    # defer() -- Es el opuesto al values method
    # Este metodo nos permite aplazar la carga de ciertos campos para después

    #Este ejemplo sería que queremos todos los campos menos el descripcipon este sería luego
    query_set = Product.objects.defer('description')

    return render(request, "hello.html",{'name': 'Mosh', 'products': query_set})


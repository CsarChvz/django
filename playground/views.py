from django.shortcuts import render
from django.http import HttpResponse

from store.models import Collection, Order, OrderItem, Product, Customer
# Create your views here.
def say_hello(request):
    # Usamos "select_related" cuando cuando el otro fin de la relacion tiene una instancia
    # POR EJEMPLO EN PRODUCT, NADA MAS TIENE UNA COLLECION - O SEA QUE UN PRODUCTO TIENE UNA COLLECION
    # En otro caso usamos "prefetch_related" cuando el otro fin de la relación tiene varios objetos/instancias
    # LAS PROMOCIONES DE UN PRODUCTO, O SEA QUE UN PRODUCTO PUEDE ESTAR EN VARIAS PROMOCIONES Y UNA PROMOCION PUEDE TENER VARIOS PRODUCTOS

    # Selecting releated objects -- Seleccionando objetos relacionados
    # A veces tenemos que pre-cargar un montón de objetos juntos 
    # Mandar a llamar un campo de otro objeto de una foreignKey?
    # Algo así se hace con select_related
    # Ya que Django solo va a hacer query en la tabla, al menos que se le diga que no

    # Se pone en el parametro el campo que queremos precargar
    query_set = Product.objects.select_related('collection').all()

        # ¿Qué hace?
        # Este metodo hace un innerjoin entre la tabla store_product y la tabla store_collection
    # También podemos expandir relaciones, por ejemplo que collection tenga otro campo que queremos precargar
    # en el parametro seerúa poner asi .select_related('collection__someOtherField')

    # --- Prefetch_related ---
    #  # En otro caso usamos "prefetch_related" cuando el otro fin de la relación tiene varios objetos/instancias
    # Se usa para precargar las promociones
    query_set = Product.objects.prefetch_related('promotions').select_related('collection').all()
    return render(request, "hello.html",{'name': 'Mosh', 'products': query_set})


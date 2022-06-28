from ast import Or
from django.shortcuts import render
from django.http import HttpResponse
from store.models import Collection, Order, OrderItem, Product, Customer
# Create your views here.
def say_hello(request):
    query_set = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
    return render(request, "hello.html",{'name': 'Mosh', 'products': list(query_set)})

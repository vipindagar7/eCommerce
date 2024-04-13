from django.shortcuts import render
from shop.models import Product


def index(request):
    products = Product.objects.order_by('?')[:5]
    return render(request , 'index.html' , {'products': products})

def about(request):
    return render(request , 'about.html')
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F
from store.models import *


def get_inventory():
    # return inventory less than 10
    query_inventory = Product.objects.filter(inventory__gt=10)
    return list(query_inventory)


def get_order():
    # return list of order made by customer with id=1
    query_order = Order.objects.filter(customer__id=1)
    return list(query_order)


def get_collection():
    # Collection that doesn't have a featured product
    collection_query = Collection.objects.filter(featured_product__isnull=True)
    return list(collection_query)


def queryby():
    # Products : inventory < 10 and price < 20
    queryby_inv_and_price = Product.objects.filter(
        inventory__lt=10, unit_price__lt=20)
    return list(queryby_inv_and_price)


def query_by_env_eq_price():
    querybyenv_price = Product.objects.filter(inventory=F('unit_price'))
    return list(querybyenv_price)


def say_hello(request):
    # filter by collection.id=1 __ is called lookup type
    # collection_query = Product.objects.filter(collection__id=1)

    last_update_query = Product.objects.filter(last_update__year=2020)

    # keyword=value get all product with unit price in rage (20,30)
    # queryset = Product.objects.filter(unit_price__range=(20, 30))

    return render(request, 'hello.html', {'products': query_by_env_eq_price})


def product(request):
    # Short product by title
    query_order = Product.objects.order_by('title')

    # value to return fields we want
    query_value = Product.objects.values('id', 'title', 'collection__title')
    return render(request, 'product.html', {'products': list(query_value)})


def limit_product(request):
    # limit the result to 5 objects
    query_order = Product.objects.all()[:5]

    # Product tha was order and short them by title
    queryset = Product.objects.filter(id__in=OrderItem.objects.values(
        'product_id').distinct()).order_by('title')

    return render(request, 'product.html', {'products': list(queryset)})

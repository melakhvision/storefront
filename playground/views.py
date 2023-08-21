from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Func, Value, ExpressionWrapper, DecimalField
from django.db import transaction
import json
from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedItem
from django.db.models.functions import Concat
from django.db.models.aggregates import Count, Max, Min, Avg, Sum

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


def say_hellos(request):
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

    # Product tha was ordered and short them by title
    queryset = Product.objects.filter(id__in=OrderItem.objects.values(
        'product_id').distinct()).order_by('title')

    return render(request, 'product.html', {'products': list(queryset)})


def collection(request):
    # limit the result to 5 objects
    query_order = Product.objects.all()[:5]

    # Product with our collection
    queryset = Product.objects.select_related('collection').all()

    return render(request, 'collection.html', {'products': list(queryset)})


def order_with_customer_in_product(request):
    # Get last 5 order with their customer and items include products
    queryset = Order.objects.select_related(
        'customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
    return render(request, 'collection.html', {'orders': list(queryset)})


def extra_query(request):
   # COunt number of product diplay key value by default as "id__count" but can be chnaged as shown
    result1 = Product.objects.aggregate(count=Count('id'))

    # count how many order we have
    result2 = Order.objects.aggregate(count=Count('id'))

    # How many units of product 1 have we sold
    result3 = OrderItem.objects.filter(
        product__id=1).aggregate(units_sold=Sum('quantity'))

    # COunt haw many orders customer 1 has placed
    result4 = Order.objects.filter(customer__id=1).aggregate(
        customer_1_orders_count=Count('id'))

    # The minimum price of products in collection 3
    result4 = Product.objects.filter(
        collection__id=3).aggregate(min=Min('unit_price'))

    # The maximum price of products in collection 3
    result5 = Product.objects.filter(
        collection__id=3).aggregate(max=Max('unit_price'))

    # The avrage price of products in collection 3
    result = Product.objects.filter(
        collection__id=3).aggregate(avg=Avg('unit_price'))

    # Add new field in_new in our Customer table

    queryset1 = Customer.objects.annotate(in_new=Value(True))

    # Create full_name from from first_name and last_name fileds methode1
    queryset2 = Customer.objects.annotate(
        full_name=Func(F('first_name'), Value(
            ' '), F('last_name'), function='CONCAT')

    )

    # Create full_name from from first_name and last_name fileds method2 - Shorter
    # Django database functions
    queryset2 = Customer.objects.annotate(
        full_name=Concat('first_name', Value(' '), 'last_name')
    )
    # payapi.fasto.bike
    # Expression wrapper
    discounted_price = ExpressionWrapper(
        F('unit_price') * 0.8, output_field=DecimalField())
    queryset3 = Product.objects.annotate(
        discount_price=discounted_price
    )

    # TOP best-selling product and their total sales
    queryset = Product.objects.annotate(total_sales=Sum(
        F('oderitem__unit_price') * F('oderitem__quantity')
    )).order_by('-total_sales')[:5]

    return render(request, 'hello.html', {'result': result})


def cache_query(request):
    # the query
    queryset = Product.objects.all()
    # cache in memory
    list(queryset)
    # access it
    queryset[0]
    return render(request, 'hello.html', {'result': list(queryset)})


def say_hello(request):
    # show tags in Product that are in Product for the id 1
    queryset = TaggedItem.objects.get_tags_for(Product, 1)

    collection = Collection()
    collection.title = 'Video Games'
    collection.featured_product = Product(pk=1)
    collection.save()
    return render(request, 'hello.html', {'result': list(queryset)})


def update_product(request):
    # methods 1 for updating
    # collection = Collection.objects.get(pk=11)
    # collection.featured_product = None
    # collection.save()

    # method 2 for updating
    Collection.objects.filter(pk=11).update(featured_product=None)
    return render(request, 'hello.html', {'result': "thiane"})


def delete_product(request):
    # methods 1 for deleting
    collection = Collection.objects.filter(pk=11)
    collection.delete()

    # # Methods to for deleting this not gonna work because of our database model
    Collection.objects.filter(id__gt=5).delete()
    return render(request, 'hello.html', {'result': "thiane"})


def create_cart_item(request):
    # create the cart first
    # cart = Cart()
    # cart.save()
    cart_item = CartItem()
    cart_item.product = Product(pk=5)
    cart_item.cart = Cart(pk=1)
    cart_item.quantity = 5
    cart_item.save()
    return render(request, 'hello.html', {'result': "thiane"})


def update_cart_item(request):
    # updating cart item quantity 2
    cart_item = CartItem.objects.get(pk=1)
    cart_item.quantity = 2
    cart_item.save()
    return render(request, 'hello.html', {'result': "thiane"})


def remove_shopping_cart(request):
    cart_item = CartItem.objects.get(pk=1)
    cart_item.delete()
    return render(request, 'hello.html', {'result': "thiane"})


def create_order(request):
    # transaction prevent partial commit on the query
    with transaction.atomic():
        order = Order()
        order.customer_id = 1
        order.save()

        item = OrderItem()
        item.order = order
        item.product_id = 2
        item.quantity = 1
        item.unit_price = 10
        item.save()
    return render(request, 'hello.html', {'result': "thiane"})


def health_check(request):
    # return HttpResponse(json.dumps({'response': 'running fine'}), status=200)
    return HttpResponse('running fine', status=200)

from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpRequest

# django_filters need to added to INSTALLED_APPS
from django_filters.rest_framework import DjangoFilterBackend

from django.db.models.aggregates import Count
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework import generics
from rest_framework.decorators import action

from rest_framework import authentication, permissions

from rest_framework.decorators import action, APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny


from store.filters import ProductFilter

from .permissions import IsAdminorReadonly, ViewCustomerHistory
from .models import Cart, CartItem, Customer, Order, Product, Collection, OrderItem, Review
from .serializers import CreateOrderSerializer, CustomerSerializer, AddCartItemSerializer, OrderSerializer, ReadOnlyCustomerSerializer, UpdateCartItemSerializer, CartItemSerializer, CartSerializer, ProductSerializer, CollectionSerializer, ReviewSerializer, UpdateOrderSerializer
# Create your views here.


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # custom permission in permissions.py file
    permission_classes = [IsAdminorReadonly]
    # start filter and search
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    # 'PAGE_SIZE': 10 need to be added to REST_FRAMEWORK in settings.py
    pagination_class = PageNumberPagination
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']
    # end filter and search

    # custom filter
    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=collection_id)
    #     return queryset

    def destroy(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs['pk'])
        if product.orderitems.count() > 0:
            return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class CollectViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminorReadonly]

    def destroy(self, request, *args, **kwargs):
        collection = get_object_or_404(Collection, pk=kwargs['pk'])
        if collection.products.count() > 0:
            return Response({"error": "Collection cannot be delete because include some products"})
        return super().destroy(request, *args, **kwargs)

    # Passing custom serializer depending on methods
    # def get_serializer_class(self):
    #     if self.request.method == 'POST':
    #         return PostCollectionSerializer
    #     return CollectionSerializer

    # def get(self, request):
    #     collections = Collection.objects.annotate(
    #         products_count=Count('products')).all()
    #     serializer = CollectionSerializer(collections, many=True)
    #     return Response(serializer.data)

    # def post(self, request: HttpRequest):
    #     serializer = PostCollectionSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(
#         products_count=Count('products'))
#     serializer_class = CollectionSerializer

#     def delete(self, request: HttpRequest, pk):
#         collection = get_object_or_404(Collection.objects.annotate(
#             products_count=Count('products')), pk=pk)
#         if collection.products.count() > 0:
#             return Response({"error": "Collection cannot be delete because include some products"})
#         else:
#             collection.delete()
#             return Response({"message": "deleted successfully"}, status=status.HTTP_200_OK)
# CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet

# samples using (APIView)

# class ProductList(APIView):
#     def get(self, request: HttpRequest):
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def post(self, request: HttpRequest):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

class ReviewViewset(ModelViewSet):
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminorReadonly]
    # getting the prodcut_id from the query params and store it
    # use it in ReviewSerializer in serializers.py

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


# Get not supported on this endpoint
# ,
class CartViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    # store cart_id with the value with the pk we get from the query
    # pass to the save serializer with cart_id = self.context['cart_id']
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return ReadOnlyCustomerSerializer
        return CustomerSerializer

    # get from django permission in group
    permission_classes = [permissions.IsAdminUser]

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         # becarefull this should return an aray of object not or array of string
    #         return [AllowAny()]

    @action(detail=True, permission_classes=[ViewCustomerHistory])
    def history(self, request: HttpRequest, pk):
        return Response('ok')

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request: HttpRequest):
        (customer, created) = Customer.objects.get_or_create(
            user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = ReadOnlyCustomerSerializer(
                customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data,
            context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()

        customer_id = Customer.objects.only(
            'id').get(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)

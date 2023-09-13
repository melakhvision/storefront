from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.db.models.aggregates import Count

# ##simple use need api_view
# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, GenericAPIView

from rest_framework.mixins import ListModelMixin, CreateModelMixin

from rest_framework.views import APIView


from .models import Product, Collection, DeletedResponse
from .serializers import ProductSerializer, CollectionSerializer, PostCollectionSerializer
# Create your views here.


class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class ProductDetail(APIView):
    def get(self, request: HttpRequest, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request: HttpRequest, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: HttpRequest, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0:
            return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            product.delete()
            return HttpResponse({"message": "product deleted"}, status=status.HTTP_204_NO_CONTENT)


class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCollectionSerializer
        return CollectionSerializer

    def get_serializer_context(self):

        return ({'request': self.request})
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


class CollectionDetail(APIView):

    def get(self, request: HttpRequest, id):
        collection = get_object_or_404(Collection.objects.annotate(
            products_count=Count('products')), pk=id)
        serializer = CollectionSerializer(collection)
        return Response(data=serializer.data)

    def delete(self, request: HttpRequest, id):
        collection = get_object_or_404(Collection.objects.annotate(
            products_count=Count('products')), pk=id)
        if collection.products.count() > 0:
            return Response({"error": "Collection cannot be delete because include some products"})
        else:
            collection.delete()
            return Response({"message": "deleted successfully"}, status=status.HTTP_200_OK)


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

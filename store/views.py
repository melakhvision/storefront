from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.db.models.aggregates import Count

# ##simple use need api_view
# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView

from rest_framework.mixins import ListModelMixin, CreateModelMixin

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet


from .models import Product, Collection, DeletedResponse, OrderItem
from .serializers import ProductSerializer, CollectionSerializer, PostCollectionSerializer
# Create your views here.


class ProductList(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0 :

    def delete(self, request: HttpRequest, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            product.delete()
            return HttpResponse({"message": "product deleted"}, status=status.HTTP_204_NO_CONTENT)


class CollectViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer

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

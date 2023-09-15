# storefront
install pipenv with 
```bash
pip install pipenv
```
## Install requirements from Pipfile
```bash
pipenv install
```
## convert pipfile and pipfile.lock to requirements.txt

```bash
pipenv lock -r > requirements.txt
```



### Fix django mysql connection issue on Dockerfile
```bash
RUN apk add gcc musl-dev mariadb-dev
```



```py

    # def list(self, request: HttpRequest):
    #     id = request.query_params.get('id')
    #     if id is not None:
    #         cart = get_object_or_404(Cart, id=id)
    #         serializer = CartSerializer(cart)
    #         return Response(serializer.data)
    #     queryset = Cart.objects.all()
    #     serializer = CartSerializer(queryset, many=True)
    #     return Response(serializer.data)

    # def delete(self, request: HttpRequest):
    #     id = request.query_params.get('id')
    #     cart = get_object_or_404(Cart, id=id)
    #     cart.delete()
    #     return Response(data="deleted successfully")

    # def get_queryset(self):
    #     queryset = Cart.objects.prefetch_related('items__product').all()
    #     id = self.request.query_params.get('id')
    #     if id is not None:
    #         queryset = queryset.filter(id=id)
    #         return queryset
    #     return queryset



    # def get_queryset(self):
    #     queryset = Cart.objects.prefetch_related('items__product').all()
    #     id = self.request.query_params.get('id')

    #     if id is not None:
    #         queryset = queryset.filter(id=id)
    #         return queryset
    #     return queryset

    # def destroy(self, request, pk):
    #     object = self.get_object(pk)
    #     object.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
```
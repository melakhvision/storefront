from django.urls import path, include
from . import views

# drf-nested-routers package
from rest_framework_nested import routers

# use router
router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectViewSet)
router.register('carts', views.CartViewSet, basename='carts')

products_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewset,
                         basename='product-reviews')
carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='carts-items')

# URLConf
urlpatterns = router.urls + products_router.urls + carts_router.urls


# URLConf
# urlpatterns = [
#     path('', include(router.urls)),
#     path('carts/', views.CartViewSet.as_view()),
#     path('carts/(?id=<int:id>)/', views.CartViewSetDetail.as_view())
#     #     path('products/<int:pk>/', views.ReviewViewset.)

#     #     # path('collections/', views.CollectViewSet.as_view()),
#     #     # path('collections/<int:pk>/', views.CollectViewSet.as_view())

# ]

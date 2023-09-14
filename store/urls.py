from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# use simple route
router = DefaultRouter()
# router.register('products', views.ProductList)
router.register('collections', views.CollectViewSet)


# URLConf
urlpatterns = [
    path('', include(router.urls)),
    path('products/', views.ProductList.as_view()),
    path('products/<int:pk>/', views.ProductDetail.as_view())
    # path('collections/', views.CollectViewSet.as_view()),
    # path('collections/<int:pk>/', views.CollectViewSet.as_view())

]

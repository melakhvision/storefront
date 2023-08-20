from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('product/', views.product),
    path('limit/', views.limit_product),
    path('hello/', views.say_hello),
    # path('collection/', views.collection),
    path('collection/', views.order_with_customer_in_product)
]

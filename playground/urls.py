from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('product/', views.product),
    path('limit/', views.limit_product),

    path('hello/', views.say_hello)
]

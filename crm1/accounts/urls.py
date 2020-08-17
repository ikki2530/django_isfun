from django.urls import path
from accounts.views import home, products, customer

urlpatterns = [
    path('', home),
    path('customer/', customer),
    path('products/', products),
]

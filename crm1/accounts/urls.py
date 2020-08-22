from django.urls import path
from accounts.views import home, products, customer, createOrder, updateOrder, deleteOrder

urlpatterns = [
    path('', home, name="home"),
    # passing parameter
    path('customer/<str:pk_test>', customer, name="customer"),
    # name es utilizado para las urls dentro de la página(botones)
    path('products/', products, name="products"),
    path('create_order/<str:pk>/', createOrder, name="create_order"),
    path('update_order/<str:pk>/', updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', deleteOrder, name="delete_order"),
    
]

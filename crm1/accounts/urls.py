from django.urls import path

from django.contrib.auth import views as auth_views

from accounts.views import home, products, customer, createOrder, updateOrder, deleteOrder
from accounts.views import registerPage, loginPage, logoutUser, userPage, accountSettings
urlpatterns = [
    path('register/', registerPage, name="register"),
    path('login/', loginPage, name="login"),
    path('logout/', logoutUser, name="logout"),
    path('', home, name="home"),
    path('user/', userPage, name="user-page"),
    # profile view
    path('account/', accountSettings, name="account"),
    # passing parameter
    path('customer/<str:pk_test>', customer, name="customer"),
    # name es utilizado para las urls dentro de la página(botones)
    path('products/', products, name="products"),
    path('create_order/<str:pk>/', createOrder, name="create_order"),
    path('update_order/<str:pk>/', updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', deleteOrder, name="delete_order"),
    # password reset
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset.html"),
        name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_sent.html"),
        name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_form.html"),
        name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_done.html"),
        name="password_reset_complete"), 
]

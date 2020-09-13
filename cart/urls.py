from django.urls import path
from cart import views

urlpatterns = [
    path('', views.index, name='index'),
    path('deneme', views.deneme, name='deneme'),
    path('cart-add/<int:id>', views.cart_add, name='cart_add'),
    path('cart-remove/<int:id>', views.cart_remove, name='cart_remove'),
    path('cart-detail', views.cart_detail, name='cart_detail'),
]

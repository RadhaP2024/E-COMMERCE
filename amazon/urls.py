from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:id>/', views.product_details, name='product_details'),
    path('add/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/increase/<int:id>/', views.increase, name='increase'),
    path('cart/decrease/<int:id>/', views.decrease, name='decrease'),
    path('cart/remove/<int:id>/', views.remove, name='remove'),
]
from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartPageView.as_view(), name='cart'),
    path('add_cart/<int:product_id>', views.AddToCartPageView.as_view(), name='add_cart'),
]
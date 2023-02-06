from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartPageView.as_view(), name='cart'),
    path('add_cart/<int:product_id>', views.AddToCartPageView.as_view(), name='add_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.RemoveCart.as_view(), name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.RemoveCartItem.as_view(), name='remove_cart_item'),
    path('checkout', views.CheckoutPageView.as_view(), name='checkout'),
]
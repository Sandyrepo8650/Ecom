from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('store', views.StorePageView.as_view(), name='store'),
    path('product-detail/<slug:slug>', views.ProductDetailPageView.as_view(), name='product-detail'),
]
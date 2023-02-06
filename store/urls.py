from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('store', views.StorePageView.as_view(), name='store'),
    path('store/<slug:slug>', views.StorePageView.as_view(), name='product_by_category'),
    path('product-detail/<slug:slug>', views.ProductDetailPageView.as_view(), name='product-detail'),
    path('search', views.SearchPageView.as_view(), name='search'),
    path('dashboard', views.DashboardPageView.as_view(), name='dashboard'),
]
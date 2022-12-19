from django.shortcuts import render
from django.views import View
from .models import Product
from category.models import Category
from cart.models import Cart, CartItem


class HomePageView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all().order_by('-created_date')[:8]
        context = {'products': products}
        return render(request, 'products/index.html', context)


class StorePageView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all().order_by('-created_date')
        total_products = products.count()
        context = {
            'products': products,
            'total': total_products
        }
        return render(request, 'products/store.html', context)


class ProductDetailPageView(View):
    def get(self, request, slug, *args, **kwargs):
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise ValueError(f'{self.product} is not available')
        context = {'product': product}
        return render(request, 'products/product-detail.html', context)
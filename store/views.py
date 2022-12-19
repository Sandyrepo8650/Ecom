from django.shortcuts import render
from django.views import View
from .models import Product
from category.models import Category
from cart.models import Cart, CartItem


class HomePageView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'products/index.html', context)


class StorePageView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'products/store.html', context)



class ProductDetailPageView(View):
    def get(self, request, slug, *args, **kwargs):
        try:
            product = Product.objects.get(slug=slug)
            total_product = product.count()
        except Product.DoesNotExist:
            raise ValueError(f'{self.product} is not available')
        context = {'product': product, 'total_product': total_product}
        return render(request, 'products/product-detail.html', context)
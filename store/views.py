from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from .models import Product
from django.db.models import Q
from category.models import Category


class HomePageView(View):
    def get(self, request, *args, **kwargs):
        # print(dir(request))
        products = Product.objects.all()[:8]
        context = {'products': products}
        return render(request, 'products/index.html', context)


class StorePageView(View):
    def get(self, request, slug=None, *args, **kwargs):
        category = None
        products = None
        if slug != None:
            # category = Category.objects.get(slug=slug)
            category = get_object_or_404(Category, slug=slug)
            products = Product.objects.filter(category=category, is_available=True)
            total_products = products.count()
        else:
            products = Product.objects.filter(is_available=True)
            total_products = products.count()
        paginator = Paginator(products, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'products': page_obj,
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


class SearchPageView(View):
    def get(self, request, *args, **kwargs):
        if 'keyword' in request.GET:
            keyword = request.GET['keyword']
            if keyword:
                products = Product.objects.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword))
                total_products = products.count()

        context = {
            'products': products,
            'total': total_products
        }
        return render(request, 'products/store.html', context)

class DashboardPageView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'products/dashboard.html', context)
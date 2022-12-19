from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'category', 'is_available']

admin.site.register(Product, ProductAdmin)
from django.contrib import admin
from .models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id',)
    readonly_fields = ('cart_id',)

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
from django.shortcuts import render, redirect
from django.views import View
from store.models import Product
from .models import Cart, CartItem



class AddToCartPageView(View):

    def _cart_id(self, request):
        cart = request.session.session_key
        if not cart:
            cart = request.session.create()
        return cart

    def get(self, request, product_id, *args, **kwargs):
        product = Product.objects.get(id=product_id)
        try:
            cart = Cart.objects.get(cart_id = self._cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = self._cart_id(request)   
            )
            cart.save()

        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                cart = cart,
                quantity = 1
            )
            cart_item.save()
        return redirect('')


class CartPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'cart/cart.html')
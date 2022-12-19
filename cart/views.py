from django.shortcuts import render, redirect
from django.views import View
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse



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
        return redirect('cart:cart')


class CartPageView(View):

    def _cart_id(self, request):
        cart = request.session.session_key
        if not cart:
            cart = request.session.create()
        return cart

    def get(self, request, *args, **kwargs):
        total = 0
        cart_items = None
        quantity = 0
        try:
            cart = Cart.objects.get(cart_id=self._cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
        except ObjectDoesNotExist:
            pass
        context = {
            'cart_items': cart_items,
            'total': total,
            'quantity': total
        }
        return HttpResponse(cart_items.product)

        # return render(request, 'cart/cart.html')
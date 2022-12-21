from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

class AddToCartPageView(View):
    def get(self, request, product_id, *args, **kwargs):
        product = Product.objects.get(id=product_id)
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request))
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


class RemoveCart(View):
    def get(self, request, product_id, *args, **kwargs):
        product = Product.objects.get(id=product_id)
        cart = get_object_or_404(Cart, cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)
        
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('cart:cart')


class RemoveCartItem(View):
    def get(self, request, product_id, *args, **kwargs):
        cart = get_object_or_404(Cart, cart_id = _cart_id(request))
        product = Product.objects.get(id=product_id)
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.delete()
        return redirect('cart:cart')


class CartPageView(View):
    def get(self, request, *args, **kwargs):
        total = 0
        cart_items = None
        quantity = 0
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
            total_with_tax = (total * 0.18)
            total_cost = (total + total_with_tax)
        except ObjectDoesNotExist:
            pass
        context = {
            'cart_items': cart_items,
            'total': total,
            'quantity': total,
            'total_with_tax': total_with_tax,
            'total_cost': total_cost
        }
        # return HttpResponse(product_title)

        return render(request, 'cart/cart.html', context)
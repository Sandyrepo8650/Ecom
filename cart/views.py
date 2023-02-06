from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.mixins import LoginRequiredMixin


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


class AddToCartPageView(View):
    def get(self, request, product_id, *args, **kwargs):
        product = Product.objects.get(id=product_id)
        return redirect('cart:cart')
    
    def post(self, request, product_id, *args, **kwargs):
        current_user = request.user
        product = Product.objects.get(id=product_id)
        if current_user.is_authenticated:
            product_variation = []
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variations = Variation.objects.get(variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variations)
                except:
                    pass
            is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
            if is_cart_item_exists:
                cart_item = CartItem.objects.filter(product=product, user=current_user)
                exist_var_list = []
                id = []
                for item in cart_item:
                    exisiting_variation = item.variation.all()
                    exist_var_list.append(list(exisiting_variation))
                    id.append(item.id)
                if product_variation in exist_var_list:
                    print('extenting quantity')
                    index = exist_var_list.index(product_variation)
                    item_id = id[index]
                    item = CartItem.objects.get(product=product, id=item_id)    
                    item.quantity += 1
                    item.save()
                else:
                    print('creating new item')
                    item = CartItem.objects.create(product=product, quantity = 1, user=current_user)
                    if len(product_variation) > 0:
                        item.variation.clear()
                        item.variation.add(*product_variation)
                    item.save()

            else:
                cart_item = CartItem.objects.create(
                    product=product,
                    user=current_user,
                    quantity = 1
                )
                cart_item.variation.clear()
                if len(product_variation) > 0:
                    cart_item.variation.add(*product_variation)
                cart_item.save()
            # if user is not authenticated
        else:
            product_variation = []
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variations = Variation.objects.get(variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variations)
                except:
                    pass
            try:
                cart = Cart.objects.get(cart_id = _cart_id(request))
                
            except Cart.DoesNotExist:
                cart = Cart.objects.create(
                    cart_id = _cart_id(request)   
                )
                cart.save()
            is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
            if is_cart_item_exists:
                cart_item = CartItem.objects.filter(product=product, cart=cart)
                exist_var_list = []
                id = []
                for item in cart_item:
                    exisiting_variation = item.variation.all()
                    exist_var_list.append(list(exisiting_variation))
                    id.append(item.id)
                if product_variation in exist_var_list:
                    print('extenting quantity')
                    index = exist_var_list.index(product_variation)
                    item_id = id[index]
                    item = CartItem.objects.get(product=product, id=item_id)    
                    item.quantity += 1
                    item.save()
                else:
                    print('creating new item')
                    item = CartItem.objects.create(product=product, quantity = 1, cart=cart)
                    if len(product_variation) > 0:
                        item.variation.clear()
                        item.variation.add(*product_variation)
                    item.save()

            else:
                cart_item = CartItem.objects.create(
                    product=product,
                    cart = cart,
                    quantity = 1
                )
                cart_item.variation.clear()
                if len(product_variation) > 0:
                    cart_item.variation.add(*product_variation)
                cart_item.save()

        return redirect('cart:cart')


class RemoveCart(View):
    def get(self, request, product_id, cart_item_id, *args, **kwargs):
        product = Product.objects.get(id=product_id)
        try:
            if request.user.is_authenticated:
                cart_item = CartItem.objects.get(product=product, id=cart_item_id, user=request.user)
            else:
                cart = get_object_or_404(Cart, cart_id=_cart_id(request))
                cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
            
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        except:
            pass
        return redirect('cart:cart')


class RemoveCartItem(View):
    def get(self, request, product_id, cart_item_id, *args, **kwargs):
        product = Product.objects.get(id=product_id)
        try:
            if request.user.is_authenticated:
                cart_item = CartItem.objects.get(product=product, id=cart_item_id, user=request.user)
            else:
                cart = get_object_or_404(Cart, cart_id = _cart_id(request))
                cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
                cart_item.delete()
        except:
            pass
        return redirect('cart:cart')


class CartPageView(View):
    def get(self, request, *args, **kwargs):
        total = 0
        cart_items = None
        quantity = 0
        cost_with_tax = 0
        total_cost = 0
        try:
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            else:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
            cost_with_tax = (total * 0.18)
            total_cost = (total + cost_with_tax)
        except ObjectDoesNotExist:
            pass
        context = {
            'cart_items': cart_items,
            'total': total,
            'quantity': total,
            'total_with_tax': cost_with_tax,
            'total_cost': total_cost
        }
        return render(request, 'cart/cart.html', context)


class CheckoutPageView(LoginRequiredMixin, View):
    login_url = 'accounts:login'
    def get(self, request, *args, **kwargs):
        total = 0
        cart_items = None
        quantity = 0
        total_with_tax = 0
        total_cost = 0
        try:
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            else:
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
        return render(request, 'cart/checkout.html', context)
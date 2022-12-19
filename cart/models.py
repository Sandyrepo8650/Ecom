from django.db import models
from store.models import Product


class Cart(models.Model):
    cart_id = models.CharField(max_length=70)
    added_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_avtive = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.product} -> {self.cart}'
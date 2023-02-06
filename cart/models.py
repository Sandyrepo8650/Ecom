from django.db import models
from store.models import Product, Variation
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Cart(models.Model):
    cart_id = models.CharField(max_length=70)
    added_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.product} -> {self.cart}'
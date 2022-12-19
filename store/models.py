from django.db import models
from category.models import Category


class Product(models.Model):
    title = models.CharField('Product Title', max_length=220, unique=True)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField()
    price = models.IntegerField()
    is_available = models.BooleanField(default=True)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='image/store/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
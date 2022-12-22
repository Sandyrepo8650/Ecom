from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=70, unique=True)
    slug = models.SlugField(max_length=70, unique=True)
    image = models.ImageField(upload_to='image/category')
    description = models.TextField()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


    def __str__(self):
        return self.title

    @property
    def get_url(self):
        return reverse("store:product_by_category", kwargs={"slug": self.slug})
    

    
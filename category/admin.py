from django.contrib import admin
from .models import Category


class CategoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}
    list_display = ('title', 'slug')

admin.site.register(Category, CategoryModelAdmin)
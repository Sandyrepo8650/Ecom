from .models import Category

def menu_links(request):
    category = Category.objects.all()
    return {
        'categories': category
    }
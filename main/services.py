from django.conf import settings
from django.core.cache import cache
from .models import Category

def get_categories():
    if settings.CACHE_ENABLED:
        objects = cache.get('categories')

        if not objects:
            objects = Category.objects.all()
            cache.set('categories', objects)
    else:
        objects = Category.objects.all()

    return objects
from django.contrib import admin

from main.models import blog, Product, Category, Version


# Register your models here.
@admin.register(blog)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description',)


@admin.register(Product)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description', 'price',)


@admin.register(Category)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description',)

@admin.register(Version)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'product', 'status',)

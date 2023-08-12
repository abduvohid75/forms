from django.db import models

from users.models import User


# Create your models here.
class blog(models.Model):
    name = models.CharField(max_length=100, verbose_name='название')
    description = models.TextField(max_length=10000, verbose_name='содержимое')
    preview = models.ImageField(verbose_name='изображение', null=True)
    view_count = models.IntegerField(default=0, verbose_name='просмотры')
    is_published = models.BooleanField(default=True, verbose_name='статус публикации')
    slug = models.CharField(max_length=150, verbose_name='slug', null=True, blank=True)
    publication_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.name} {self.description}'

    class Meta:
        verbose_name = 'материал'
        verbose_name_plural = 'материалы'


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    description = models.CharField(max_length=500, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    description = models.CharField(max_length=500, verbose_name='Описание')
    image = models.ImageField(max_length=100, verbose_name='Изображение', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name='Цена')
    date_create = models.DateField(verbose_name='Дата создания', null=True, blank=True)
    date_edit = models.DateField(verbose_name='Дата последнего изменения', null=True, blank=True)
    is_published = models.BooleanField(verbose_name='Статус публикации', default=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        permissions = [
            ('set_published', 'Can publish post'),
            ('change_desc', 'Can change description'),
            ('change_cat', 'Can change category'),
        ]


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    number = models.IntegerField(verbose_name="Версия")
    name = models.CharField(max_length=100, verbose_name="Имя версии")
    status = models.BooleanField(verbose_name="Статус")

    def __str__(self):
        return f'{self.name} {self.product} {self.status}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'

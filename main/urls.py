from django.urls import path

from main.apps import MainConfig
from main.views import BlogListView, contacts, BlogCreateView, BlogDetailView, BlogUpdateView, BlogDeleteView, \
    ProductListView, ProductCreateView

app_name = MainConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('blogs', BlogListView.as_view(), name='blogs'),
    path('create', BlogCreateView.as_view(), name='create_blogs'),
    path('product/create', ProductCreateView.as_view(), name='create_products'),
    path('contacts', contacts, name='contacts'),
    path('view/<int:pk>/', BlogDetailView.as_view(), name='view'),
    path('edit/<int:pk>/', BlogUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete'),
]

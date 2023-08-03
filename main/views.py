import pytils.translit
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from main.models import blog, Product
from main.forms import BlogForm, ProductForm


# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = 'main/index.html'
    extra_context = {'title': 'Главная'}

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('main:index')
    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = pytils.translit.slugify(new_mat.name)
            new_mat.save()
        return super().form_valid(form)

class BlogListView(ListView):
    model = blog
    template_name = 'main/view_blogs.html'
    extra_context = {'title': 'Блоги'}

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogCreateView(CreateView):
    model = blog
    form_class = BlogForm
    success_url = reverse_lazy('main:blogs')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = pytils.translit.slugify(new_mat.name)
            new_mat.save()
        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = blog
    form_class = BlogForm
    success_url = reverse_lazy('main:blogs')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = pytils.translit.slugify(new_mat.name)
            new_mat.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main:view', args=[self.kwargs.get('pk')])


class BlogDetailView(DetailView):
    model = blog
    extra_context = {'title': 'Материал'}

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object


class BlogDeleteView(DeleteView):
    model = blog
    success_url = reverse_lazy('main:blogs')


def contacts(request):
    if (request.method == 'POST'):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        print(f'Имя: {name} Email: {email} Сообщение: {message}')

    context = {
        'title': 'Контакты'
    }

    return render(request, 'main/contacts.html', context)

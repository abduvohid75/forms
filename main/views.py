import pytils.translit
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.forms import inlineformset_factory
from django.contrib.auth.models import Group

from main.models import blog, Product, Version, Category
from main.forms import BlogForm, ProductForm, VersionForm, ModerProductForm, CategoryForm
from main import services


# Create your views here.

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = pytils.translit.slugify(new_mat.name)
            new_mat.save()
        return super().form_valid(form)


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    is_moder = False
    template_name = 'main/index.html'
    extra_context = {'title': 'Главная'}

    def get_queryset(self):
        query_set = super().get_queryset()
        products_with_true_status = query_set.filter(version__status=True, is_published=True).distinct()
        return products_with_true_status

    def get_context_data(self, *, object_list=None, **kwargs):

        if Group.objects.get(name='Модераторы') in self.request.user.groups.all():
            self.is_moder = True

        context_data = super().get_context_data(**kwargs)
        context_data['is_moder'] = self.is_moder

        return context_data


class ProductUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Product
    success_url = reverse_lazy('main:index')
    perms_list = ['main.set_published_Product', 'main.change_desc_Product', 'main.change_cat_Product']

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductVersionFormSet = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.POST:
            context_data['formset'] = ProductVersionFormSet(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = ProductVersionFormSet(instance=self.object)
        return context_data

    def test_func(self):
        product = self.get_object()
        return product.author == self.request.user or Group.objects.get(name='Модераторы') in self.request.user.groups.all()

    def get_form_class(self):
        if Group.objects.get(name='Модераторы') in self.request.user.groups.all():
            return ModerProductForm
        else:
            return ProductForm

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

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

class VersionCreateView(LoginRequiredMixin, CreateView):
    model = Version
    form_class = VersionForm
    success_url = reverse_lazy('main:index')

class CategoryCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    permission_required = 'main.add_Category'
    success_url = reverse_lazy('main:categories')


def check_categories(request):
    categories = services.get_categories()

    context_data = {
        'object_list' : categories,
        'title' : 'Список категорий'
    }

    print('Категории: ', categories)

    return render(request, 'main/categories.html', context_data)

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

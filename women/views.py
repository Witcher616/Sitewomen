from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView
from django.core.cache import cache

from women.forms import AddPostForm, UploadFileForm
from women.models import Women, Category, TagPost, UploadFile


# Функция представления главной страницы
# def index(request):
#     context = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': Women.published.all().select_related('cat'),
#         'cat_selected': 0,
#     }
#     return render(request, 'women/index.html', context=context)


# Класс представления главной страницы
class WomenHome(ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    paginate_by = 5
    extra_context = {
        'title': 'Главная страница',
        'cat_selected': 0,
    }

    def get_queryset(self):
        w_lst = cache.get('women_posts')
        if not w_lst:
            w_lst = self.model.published.all().select_related('cat', 'author')
            cache.set('women_posts', w_lst, 60)
        return w_lst

# def handle_uploaded_file(f):
#     with open(f'uploads/{f.name}', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


@login_required
def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            UploadFile.objects.create(file=form.cleaned_data['file'])
    else:
        form = UploadFileForm()
    context = {
        'title': 'О нас',
        'form': form,
    }
    return render(request, 'women/about.html', context=context)

# функция представления добавления статьи
# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # try:
#             #     Women.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except:
#             #     form.add_error(None, "Не удалось добавить статью")
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#
#     context = {
#         'title': 'Добавить статью',
#         'menu': menu,
#         'form': form,
#     }
#     return render(request, 'women/addpage.html', context=context)


# Класс представления добавления статьи с помощью FormView
# class AddPage(FormView):
#     form_class = AddPostForm
#     template_name = 'women/addpage.html'
#     success_url = reverse_lazy('home')
#     extra_context = {
#         'title': 'Добавить статью',
#         'menu': menu,
#     }
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)


# Класс представления добавления статьи с помощью CreateView
class AddPage(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'title': 'Добавить статью',
    }
    permission_required = 'women.add_women'

    def form_valid(self, form):
        women_obj = form.save(commit=False)
        women_obj.author = self.request.user
        return super().form_valid(form)


class UpdatePage(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Women
    slug_url_kwarg = 'post_slug'
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'title': 'Редактирование статьи',
    }
    permission_required = 'women.change_women'


@permission_required(perm='women.view_women', raise_exception=True)
def contact(request):
    return HttpResponse("<h1>Обратная связь</h1>")


# Функция представления статьи
# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#     context = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'cat_selected': 1,
#     }
#     return render(request, 'women/post.html', context=context)


# Класс представления статьи
class ShowPost(DetailView):
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Women, slug=self.kwargs[self.slug_url_kwarg], is_published=Women.Status.PUBLISHED)

# Функция представления категории
# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug=cat_slug)
#     posts = Women.objects.filter(cat_id=category.pk).select_related('cat')
#     context = {
#         'title': f'Рубрика: {category.name}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': category.pk,
#     }
#     return render(request, 'women/index.html', context=context)


# Класс представления категории
class WomenCategory(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False
    paginate_by = 5

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat', 'author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'].first().cat
        context['title'] = f'Рубрика: {cat.name}'
        context['cat_selected'] = cat.pk
        return context


# функция представления тега
# def show_tag_postlist(request, tag_slug):
#     tag = TagPost.objects.get(slug=tag_slug)
#     posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).prefetch_related('cat')
#     context = {
#         'title': f'Тег: {tag.tag}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': None,
#     }
#     return render(request, 'women/index.html', context=context)


# класс представления тега
class WomenTag(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False
    paginate_by = 5

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).prefetch_related('cat', 'author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        context['title'] = f'Тег: {tag.tag}'
        context['cat_selected'] = None
        return context


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1 style='text-align: center;'>404 Not Found</h1>")

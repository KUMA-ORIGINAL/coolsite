from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import AddPostForm, RegisterUserForm, LoginUserForm, ContactForm
from .models import *
from .utils import *

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Обратная связь', 'url_name': 'contact'},]


class WomanHome(DataMixin, ListView):
    model = Woman
    template_name = 'woman/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Woman.objects.filter(is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))


# def index(request):
#     posts = Woman.objects.all()
#     cats = Category.objects.all()
#     context = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,
#         'cats': cats,
#         'cat_selected': 0,
#     }
#     return render(request, 'woman/index.html', context=context)


def about(request):
    contact_list = Woman.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'woman/about.html', {'title': 'О сайте',
                                                'menu': menu,
                                                'page_obj': page_obj})


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             form.save()
#             return redi   rect('home')
#     else:
#         form = AddPostForm()
#     context = {
#         'title': 'Добавление статьи',
#         'menu': menu,
#         'form': form
#     }
#     return render(request, 'woman/addpage.html', context=context)


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'woman/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))


# def contact(request):
#     return HttpResponse('add')

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'woman/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super(ContactFormView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная свзяь')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


# def login(request):
#     return HttpResponse('add')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>page not found</h1')


class ShowPost(DataMixin, DetailView):
    model = Woman
    template_name = 'woman/post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


# def show_post(request, post_slug):
#     post = get_object_or_404(Woman, slug=post_slug)
#     context = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'cat_selected': post.cat_id,
#     }
#     return render(request, 'woman/post.html', context=context)


class WomanCategory(DataMixin, ListView):
    model = Woman
    template_name = 'woman/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Woman.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.id)
        return dict(list(context.items()) + list(c_def.items()))



# def show_category(request, cat_slug):
#     posts = Woman.objects.filter(cat__slug=cat_slug)
#     cats = Category.objects.all()
#
#     if len(posts) == 0:
#         raise Http404()
#     #
#     # context = {
#     #     'title': 'Отображение по рубрикам',
#     #     'menu': menu,
#     #     'posts': posts,
#     #     'cats': cats,
#     #     'cat_selected': cat_slug,
#     }
#     return render(request, 'woman/index.html', context=context)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'woman/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'woman/login.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')



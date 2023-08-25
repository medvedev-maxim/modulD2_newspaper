from typing import Any, Dict
from django.shortcuts import render, redirect
from .models import Post, Category, User
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.core.cache import cache
# import logging 

# logger = logging.getLogger(__name__)

class PostsList(ListView):
    model = Post
    template_name='news/newslist.html'
    context_object_name='posts'
    # queryset = Post.objects.order_by('-dateCreation')
    ordering = ['-dateCreation'] # сортировка с помощью дженерика
    paginate_by = 10

class PostsSearch(ListView):
    model = Post
    template_name='news/search.html'
    context_object_name='posts'
    ordering = ['-dateCreation']
    paginate_by = 5

    # метод get_context_data нужен нам для того, чтобы мы могли передать переменные в шаблон. В возвращаемом словаре context будут храниться все переменные. Ключи этого словари и есть переменные, к которым мы сможем потом обратиться через шаблон
    def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        context['categories'] = Category.objects.all()
        context['form']=PostForm()
        return context

class PostDetail(DetailView):
    model = Post
    template_name='news/newsdetail.html'
    context_object_name='post'

    def get_object(self, *args, **kwargs): # переопределяем метод получения объекта
        obj = cache.get(f'post-{self.kwargs["pk"]}', None) # кэш очень похож на словарь, и метод get действует также. Он забирает значение по ключу, если его нет, то забирает None.
 
        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        
        return obj

# дженерик для создания объекта. Надо указать только имя шаблона и класс формы, который мы написали в прошлом юните. Остальное он сделает за вас
class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    template_name = 'news/newscreate.html'
    form_class = PostForm
    success_url = '/news/'
    
    # Переопределение метода если форма заполнена верно
    # def form_valid(self, form):
    #     # Сохраняем объект модели
    #     response = super().form_valid(form)
    #     # Действия
    #     print(form.cleaned_data['title'])
    #     return response


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    template_name = 'news/newscreate.html'
    form_class = PostForm
    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
   
# дженерик для удаления товара
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    template_name = 'news/newsdelete.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy('news:posts') # не забываем импортировать функцию reverse_lazy из пакета django.urls

class PostCategoryView(DetailView):
    model = Category
    template_name='news/category.html'
    context_object_name = 'category'

class PostCategoryList(ListView):
    model = Category
    template_name='news/categorys.html'
    context_object_name = 'categorys'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        return context

@login_required
def subscribe_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)

    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user)

    # logger.error('TEXT ERROR!') # тестирование ошибок в лог
    
    return redirect('news:categorys')
    # return redirect(request.META.get('HTTP_REFERER')) # возврат к прошлой странице

@login_required
def unsubscribe_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)

    # logger.critical('TEXT CRITICAL ERROR!!!') # тестирование ошибок в лог

    if category.subscribers.filter(id=user.id).exists():
        category.subscribers.remove(user)
    
    return redirect('news:categorys')
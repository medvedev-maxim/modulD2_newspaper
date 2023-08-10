from django.shortcuts import render
from .models import Post, Category
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class PostsList(ListView):
    model = Post
    template_name='news/newslist.html'
    context_object_name='posts'
    # queryset = Post.objects.order_by('-dateCreation')
    ordering = ['-dateCreation'] # сортировка с помощью дженерика
    paginate_by = 3

class PostsSearch(ListView):
    model = Post
    template_name='news/search.html'
    context_object_name='posts'
    ordering = ['-dateCreation']
    paginate_by = 3

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

# дженерик для создания объекта. Надо указать только имя шаблона и класс формы, который мы написали в прошлом юните. Остальное он сделает за вас
class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    template_name = 'news/newscreate.html'
    form_class = PostForm

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
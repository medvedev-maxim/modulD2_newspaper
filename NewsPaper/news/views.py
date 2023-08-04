from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView

class PostsList(ListView):
    model = Post
    template_name='news/newslist.html'
    context_object_name='posts'
    queryset = Post.objects.order_by('-dateCreation')

class PostDetail(DetailView):
    model = Post
    template_name='news/newsdetail.html'
    context_object_name='post'
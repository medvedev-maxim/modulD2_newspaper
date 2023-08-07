from django.contrib import admin
from django.urls import path
from .views import PostsList, PostDetail, PostCreateView, PostUpdateView, PostDeleteView, PostsSearch

app_name = 'news'
urlpatterns = [
    path('', PostsList.as_view(), name='posts'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('search/', PostsSearch.as_view(), name='post_search'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('update/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
]

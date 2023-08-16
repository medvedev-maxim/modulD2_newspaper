from django.contrib import admin
from django.urls import path
from .views import PostsList, PostDetail, PostCreateView, PostUpdateView, PostDeleteView, PostsSearch, PostCategoryView,PostCategoryList, subscribe_category, unsubscribe_category

app_name = 'news'
urlpatterns = [
    path('', PostsList.as_view(), name='posts'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('search/', PostsSearch.as_view(), name='post_search'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('update/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
    path('category/', PostCategoryList.as_view(), name='categorys'),
    path('category/<int:pk>/', PostCategoryView.as_view(), name='category'),
    path('subscribe/<int:pk>/', subscribe_category, name='subscribe'),
    path('unsubscribe/<int:pk>/', unsubscribe_category, name='unsubscribe'),
]

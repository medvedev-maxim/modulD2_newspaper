from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment


class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('title', 'categoryType', 'dateCreation', 'rating') # оставляем только имя и цену товара
    list_filter = ('postCategory__name', 'rating') # добавляем примитивные фильтры в нашу админку
    search_fields = ['title','rating','postCategory__name'] # тут всё очень похоже на фильтры из запросов в базу


# Register your models here.
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post,PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)
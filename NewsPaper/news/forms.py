from django.forms import ModelForm
from .models import Post, Category
from django import forms

# Создаём модельную форму
class PostForm(ModelForm):
  # В класс мета, как обычно, надо написать модель, по которой будет строиться форма, и нужные нам поля. Мы уже делали что-то похожее с фильтрами
  class Meta:
    model = Post
    fields = ['categoryType','postCategory','author','title','text']
    widgets = {
        'categoryType' : forms.Select(attrs={'class': 'form-control',}),
        'postCategory' : forms.CheckboxSelectMultiple(),
        'author' : forms.Select(attrs={'class': 'form-control',}),
        'title' : forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        'text' : forms.Textarea(attrs={'class': 'form-control',}),  
    }
from django.forms import ModelForm
from .models import Post
from django import forms
from django.contrib.auth.models import User

# Создаём модельную форму
class PostForm(ModelForm):
# В класс мета, как обычно, надо написать модель, по которой будет строиться форма, и нужные нам поля. Мы уже делали что-то похожее с фильтрами
  class Meta:
    model = Post
    fields = ['categoryType','author','title','text']
    widgets = {
        'categoryType' : forms.Select(attrs={'class': 'form-control',}), 
        'author' : forms.Select(attrs={'class': 'form-control',}),
        'title' : forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        'text' : forms.Textarea(attrs={'class': 'form-control',}),  
    }
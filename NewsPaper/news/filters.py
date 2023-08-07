from django_filters import FilterSet, DateFilter # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post
 
 
# создаём фильтр
class PostFilter(FilterSet):
    dateCreation = DateFilter(
        field_name='dateCreation',
        label='Дата новости',
        lookup_expr='gte',
        input_formats=['%d-%m-%Y', '%d-%m','%m', '%d', '%m-%Y', '%d.%m.%Y'],  # Укажите желаемый формат ввода даты
        )
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т.е. подбираться) информация о товарах
    class Meta:
        model = Post
        # fields = ('categoryType','title','dateCreation', 'author') # поля, которые мы будем фильтровать (т.е. отбирать по каким-то критериям, имена берутся из моделей)
        fields = {
            'categoryType':['exact'],
		    'title': ['icontains'],
		    'author':['exact'],
        }
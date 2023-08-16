from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import PostCategory
from .tasks import new_post_subscription
from django.core.mail import send_mail
from django.conf import settings
#сигнал после сохранения. Но записи в мультиполе попадают после отрабатывания post_save, для этого еще m2m_changed


# отправка почты по сигналу
@receiver(m2m_changed, sender = PostCategory)
def notify_subscribers(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        new_post_subscription(instance)
    
    # Тестовая проверка отправки сообщения
    # send_mail(
    #     subject = f'Добавлена новая публикация!',
    #     message = f'Добавлена новая публикация {instance}',
    #     from_email = settings.DEFAULT_FROM_EMAIL,
    #     recipient_list = ['test@test.com'],
    # )
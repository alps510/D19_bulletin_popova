from django.conf.global_settings import SERVER_EMAIL
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reply, Profile


@receiver(post_save, sender=Reply)
def notify_reply_added(sender, instance, created, **kwargs):
    if created:
        subject = 'Новый отклик'
        message = f'Новый отклик {instance.content}, на статью {instance.post} автора {instance.post.user}'
        recipient = instance.post.user.email
    else:
        subject = 'Статус Вашего отклика измене'
        message = f'{instance.user}, {instance.content} - статус изменился на {instance.status}'
        recipient = instance.user.email
    send_mail(
        subject=subject,
        message=message,
        from_email='alps51@yandex.ru',
        recipient_list=[recipient]
        )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

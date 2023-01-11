from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from .my_constants import TYPE_LIST
from ckeditor_uploader.fields import RichTextUploadingField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscribe = models.BooleanField(default=False)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=11, choices=TYPE_LIST, blank=False)
    title = models.CharField(max_length=255)
    content = RichTextUploadingField()

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def preview(self):
        if len(self.content) > 124:
            return self.content[:124] + '...'
        else:
            return self.content

    def __str__(self):
        return f'{self.title}: {self.content}'


class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(default='SomeText...')
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

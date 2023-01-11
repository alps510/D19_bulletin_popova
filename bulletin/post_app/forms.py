from django.forms import ModelForm
from .models import Post, Reply
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


class PostForm(ModelForm):
    #content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = [
            'title',
            'type',
            'content',
        ]


class ReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = [
            'content',
        ]

from django.db import models
from django.forms import fields
from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = "ایمیل (نمایش داده نخواهد شد)"
        self.fields['name'].label = "نام"
        self.fields['content'].label = "محتوای کامنت"

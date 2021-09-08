from django.db import models
from django.forms import fields
from squads.models import Comment, Squad
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.core.validators import RegexValidator

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

class GroupForm(forms.ModelForm):
    class Meta:
        model = Squad
        fields = ('name', 'eng_title', 'summary', 'capacity', 'picture')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].label = ""



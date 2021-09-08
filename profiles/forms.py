
from django import forms
from profiles.models import Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm



class UserRegisterationForm(UserCreationForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(UserRegisterationForm, self).__init__(*args, **kwargs)
        self.helper = UserCreationForm()
        self.helper.form_show_labels = False 
    class Meta:
        model = get_user_model()
        fields = ['first_name','username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['gender','birthday']

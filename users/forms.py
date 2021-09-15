from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import forms

# from allauth.account import SignupForm


class CustomUserCreationForm(UserCreationForm):
    # first_name = forms.CharField(max_length=100)
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'email', 'username',)



# class CustomUserChangeForm(UserChangeForm):

#     class Meta:
#         model = get_user_model()
#         fields = ('email', 'username', 'age')


# class CustomSignUpForm(SignupForm):

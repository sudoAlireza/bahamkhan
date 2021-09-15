
from django import forms
from django.forms import fields
from profiles.models import Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm



class UserRegisterationForm(UserCreationForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(UserRegisterationForm, self).__init__(*args, **kwargs)
        self.helper = UserCreationForm()
        # self.helper.form_show_labels = False 
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'row':'3'})

    class Meta:
        model = get_user_model()
        fields = ['first_name','username', 'email', 'password1']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    def __init__(self, *args, **kwargs): 
        super(UserUpdateForm, self).__init__(*args, **kwargs)                       
        self.fields['email'].disabled = True
        self.fields['username'].disabled = True
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'row':'3',})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'row':'3'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'row':'3',})

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name']


class ProfileUpdateForm(forms.ModelForm):
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type':'date','row':'3', 'max':'2014-01-01'}))
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        # self.fields['birthday'].widget.attrs.update(
                                                    # {'type':'date',
                                                    #     'class': 'form-control',
                                                    # 'row':'3',
                                                    # }
                                                    # )
        self.fields['gender'].widget.attrs.update({'class': 'form-select'})
    
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ('slug','avatar')


class AvatarUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AvatarUpdateForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].widget.attrs.update(
            {'class': 'form-control form-control-sm',
            'row':'3',
            'type': 'file',
            # 'id': 'id_picture formFileLg',
        }
        )

    class Meta:
        model = Profile
        fields = ('avatar',)
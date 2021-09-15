from django.contrib.auth import get_user_model
from django.forms.forms import Form
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, UpdateView, View

from django.http import HttpResponseRedirect


from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from profiles.models import Profile
from .forms import AvatarUpdateForm, UserRegisterationForm, UserUpdateForm, ProfileUpdateForm



class ProfileView(DetailView):
    model = Profile
    template_name = 'profiles/profile_detail.html'
    fields = ['email', 'user']
    context_object_name = 'profile'


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(
#                 request,
#                 f'Your account has been created! You are now able to log in')
#             return redirect('/login/')
#     else:
#         form = UserRegisterationForm()
#     return render(request, 'signup.html', {'form': form})


# @login_required
# def profile(request, slug):
#     if request.method == 'POST':
#         user_form = UserUpdateForm(request.POST, instance=request.user)
#         profile_form = ProfileUpdateForm(request.POST,
#                                    request.FILES,
#                                    instance=request.user.profile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, f'Your account has been updated!')
#             return HttpResponseRedirect(f'/profile/{slug}')
#     else:
#         user_form = UserUpdateForm(instance=request.user)
#         profile_form = ProfileUpdateForm(instance=request.user.profile)

#     context = {'user_form': user_form, 'profile_form': profile_form}

#     return render(request, 'profiles/profile_edit.html', context)




class ProfileUpdate(UpdateView):
    model = Profile
    template_name = 'profiles/profile_edit.html'
    def post(self, request, slug):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        avatar_form = AvatarUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid() and avatar_form.is_valid():
            user_form.save()
            profile_form.save()
            avatar_form.save()
            return HttpResponseRedirect(f'/profile/{slug}')

    def get(self, request, slug):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        avatar_form = AvatarUpdateForm(instance=request.user.profile)
        context = {'user_form': user_form, 'profile_form': profile_form, 'avatar_form': avatar_form}
        return render(request, 'profiles/profile_edit.html', context)


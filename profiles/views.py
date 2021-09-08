from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, UpdateView

from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from profiles.models import Profile
from .forms import UserRegisterationForm, UserUpdateForm, ProfileUpdateForm



class ProfileView(DetailView):
    model = Profile
    template_name = 'profiles/profile_detail.html'
    fields = ['email', 'user']
    context_object_name = 'profile'


def register(request):
    if request.method == 'POST':
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request,
                f'Your account has been created! You are now able to log in')
            return redirect('/login/')
    else:
        form = UserRegisterationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('/profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'u_form': u_form, 'p_form': p_form}

    return render(request, 'profiles/profile.html', context)



class ProfileUpdateView(UpdateView):
    model = Profile
    template_name = 'profiles/profile_edit.html'
    success_url = reverse_lazy('profile_details')
    fields = '__all__'

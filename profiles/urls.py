from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from profiles.views import ProfileView

from .views import ProfileUpdateView, register

urlpatterns = [
    path('login/', LoginView.as_view(template_name='profiles/login.html'),
         name='login'),
    path('logout/', LogoutView.as_view(template_name='profiles/logout.html'),
         name='logout'),
    path('signup/', register, name='signup'),
    path('profile/<slug:slug>/', ProfileView.as_view(), name='profile_details'),
    path('profile/<slug:slug>/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
]

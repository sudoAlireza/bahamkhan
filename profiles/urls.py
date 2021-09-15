from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from profiles.views import ProfileView, ProfileUpdate

# from .views import register

urlpatterns = [
#     path('login/', LoginView.as_view(template_name='profiles/login.html'),
#          name='login'),
#     path('logout/', LogoutView.as_view(template_name='profiles/logout.html'),
#          name='logout'),
#     path('signup/', register, name='signup'),
    path('profile/<str:slug>/', ProfileView.as_view(), name='profile_details'),
    # path('profile/<slug:slug>/edit/', profile, name='profile_edit'),
    path('profile/<str:slug>/edit/', ProfileUpdate.as_view(), name='profile_edit'),
]

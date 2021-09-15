from django.urls import path

from .views import (
    GroupListView,
    GroupDetailView,
    CreateGroupView,
    CommentCreateView,
    GroupUpdateView,
    SearchResultListView,
    ApproveView,
    RejectView
)
from . import views

urlpatterns = [
    path('groups/', GroupListView.as_view(), name='group_list'),
    path('groups/<slug:slug>/', GroupDetailView.as_view(), name='group_detail'),
    path('create-group/', CreateGroupView.as_view(), name='new_group'),
    path('groups/<slug:slug>/join/', views.join_group, name='join-group'),
    path('groups/<slug:slug>/leave/', views.leave_group, name='leave-group'),
    path('groups/<slug:slug>/', GroupDetailView.as_view(), name='group-detail'),
    path('groups/<slug:slug>/comment/', CommentCreateView.as_view(), name='comment-create'),
    path('groups/<slug:slug>/update', GroupUpdateView.as_view(), name='group_edit'),
    path('search/', SearchResultListView.as_view(), name='search_results'),
    path('groups/<slug:slug>/<str:user_slug>/approve/', ApproveView.as_view(), name='approve'),
    path('groups/<slug:slug>/<str:user_slug>/reject/', RejectView.as_view(), name='reject')
]

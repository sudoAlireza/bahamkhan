from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from .models import Squad

class MembershipRequiredMixin:

    def dispatch(self, request,slug, *args, **kwargs):
        group = get_object_or_404(Squad, slug=slug)
        # for members in group.members.all():
        if request.user.profile in group.members.all():
            return super().dispatch(request,slug, *args, **kwargs)
        else:
            raise PermissionDenied

class GroupCreatorRequiredMixin:

    def dispatch(self, request, slug, *args, **kwargs):
        group = get_object_or_404(Squad, slug=slug)
        if self.request.user == group.creator:
            return super().dispatch(request,slug, *args, **kwargs)
        else:
            raise PermissionDenied



from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from squads.models import Squad


class HomePageView(ListView):
    template_name = 'home.html'
    model = Squad
    queryset = Squad.objects.all()[:5]
    context_object_name = 'groups_list'
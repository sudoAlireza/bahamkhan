from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, CreateView, ListView

from django.views.generic.edit import CreateView, UpdateView
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import DetailView

from squads.models import Squad, Comment, Membership
from profiles.models import Profile


from django.core.mail import EmailMessage, send_mail


from .forms import CommentForm, GroupForm
from .mixins import (
    MembershipRequiredMixin,
    GroupCreatorRequiredMixin
)


from django.db.models import Q, query
from django.contrib.auth import get_user_model


class GroupListView(View):
    model = Squad

    def get(self, request):
        squads = Squad.objects.all()
        context = {
            'groups': squads,
        }
        return render(request, 'squads/squads_list.html', context)


class ApproveView(GroupCreatorRequiredMixin, DetailView):
    def get(self, request, slug, user_slug):
        group = Squad.objects.get(slug=slug)
        that_user = group.members.get(slug = user_slug)
        # all_members = group.members.all()
        m1 = Membership.objects.get(group=group, members=that_user)
        count = group.membership_set.filter(is_approved=True).count()
        if count < group.capacity:
            m1.is_approved = True
            m1.save()
            email_subject = f'درخواست عضویت شما در گروه باهم‌خوانی {group.name} پذیرفته شد'
            email_body = f'درخواست عضویت شما در گروه {group.name} پذیرفته شده \n https://bahamkhan.ir'
            email = EmailMessage(
                email_subject,
                email_body,
                'bahamkhan.ir@gmail.com',
                (that_user.user.email,),
            )
        email.send(fail_silently=False)
        return HttpResponseRedirect(f'/groups/{slug}')


class RejectView(GroupCreatorRequiredMixin ,DetailView):
    def get(self, request, slug, user_slug):
        group = Squad.objects.get(slug=slug)
        that_user = group.members.get(slug = user_slug)
        m1 = Membership.objects.get(group=group, members=that_user)
        m1.delete()
        return HttpResponseRedirect(f'/groups/{slug}')



class GroupDetailView(DetailView):
    template_name = 'squads/squad_detail.html'
    model = Squad
    

    def get(self, request, slug):
        this_user = self.request.user
        group = Squad.objects.get(slug = slug)
        all_members = group.members.all()
        comments = group.comment_set.all()
        comment_form = CommentForm()

        members_list = list(all_members)

        # for member in all_queries:
        #     members_list.append(member.user)

        # members_list_by_profile = list(all_members)
        
        try:
            approved_member = this_user.profile.membership_set.get(group=group).is_approved
        except:
            approved_member = False
        

        # is_member = this_user.username in members_list
        is_creator = this_user == group.creator


        is_member = False
        if this_user.is_authenticated:
            if this_user.profile in members_list:
                is_member = True

        is_creator = this_user == group.creator

        unapproved_requests = list(group.membership_set.filter(is_approved=False))
        # for any_member in members_list_by_profile:
        #     if not any_member.membership_set.get(group=group).is_approved:
        #         unapproved_requests.append(any_member.membership_set.get(group=group))

        approved_requests = list(group.membership_set.filter(is_approved=True))

        # for member in all_members:
        #     member_check = Membership.objects.get(group=group, members=member)
        #     if member_check.is_approved:
        #         approved_requests.append(member)

        context = {
        'comment_form': comment_form,
        'group': group,
        'members_list': members_list,
        'comments': comments,
        'approved_member':approved_member,
        'is_member': is_member,
        'is_creator': is_creator,
        'unapproved_requests': unapproved_requests,
        'approved_requests': approved_requests,
        }
        return render(request, self.template_name, context)


class CommentCreateView(LoginRequiredMixin, MembershipRequiredMixin, View):
    login_url = '/accounts/login/' 
    def post(self, request, slug):
        group = get_object_or_404(Squad, slug=slug)
        comment = Comment(body=request.POST['body'], author= request.user, group=group)
        comment.save()
        return redirect(reverse('group-detail', args=[slug]))


@login_required(login_url='/accounts/login/')
def join_group(request, slug):
    group = Squad.objects.get(slug=slug)
    profile = Profile.objects.get(user=request.user.id)

    if group in profile.squad_set.all():
        return HttpResponseRedirect('/groups')
    # elif group.members.count() >= group.capacity:
    #     return HttpResponseRedirect('/create-group')
    else:
        membershiping = Membership.objects.create(members=profile, group=group)
        membershiping.save()
        email_subject = 'درخواست عضویت در گروه باهم‌خوان شما'
        email_body = f'کاربر {profile.user} درخواست عضویت در گروه {group.name} شما را دارد \n https://bahamkhan.ir'
        email = EmailMessage(
            email_subject,
            email_body,
            'bahamkhan.ir@gmail.com',
            (group.creator.email,),
        )
        email.send(fail_silently=False)
            
    return HttpResponseRedirect(f'/groups/{slug}')


@login_required(login_url='/accounts/login/')
def leave_group(request, slug):
    group = Squad.objects.get(slug=slug)
    profile = Profile.objects.get(user=request.user.id)

    if not group in profile.squad_set.all():
        return HttpResponseRedirect('groups/')
    else:
        group.members.remove(profile)
        if group.creator.username == profile.user.username:
            group.delete()
            return HttpResponseRedirect(reverse('group_list'))
    return HttpResponseRedirect(f'/groups/{slug}')


class CreateGroupView(LoginRequiredMixin ,CreateView):
    template_name = 'squads/new_group.html'
    model = Squad
    login_url = '/accounts/login/'
    # form_class = GroupForm
    redirect_field_name = 'redirect_to'
    def post(self, request):
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            name=request.POST['name']
            eng_title=request.POST['eng_title']
            summary=request.POST['summary']
            capacity=request.POST['capacity']
            creator=request.user
            
            if 'picture' in request.FILES:   
                picture = request.FILES['picture']
                group = Squad(name = name, eng_title=eng_title, summary=summary, capacity=capacity, creator=creator, picture=picture)
            else:
                group = Squad(name = name, eng_title=eng_title, summary=summary, capacity=capacity, creator=creator)

            creator_profile = Profile.objects.get(user=request.user.id)
            group.save()
            membershiping = Membership.objects.create(members=creator_profile, group=group)
            membershiping.is_approved = True
            membershiping.save()
            return redirect(reverse_lazy('group_detail', args=[group.slug]))

        else:
            return redirect(reverse_lazy('new_group'))
            

    def get(self, request):
        group_form = GroupForm()
        context = {
            'group_form': group_form,
        }
        return render(request, 'squads/new_group.html', context)
        

class GroupUpdateView(LoginRequiredMixin, GroupCreatorRequiredMixin, UpdateView):
    model = Squad
    template_name = 'squads/group_edit.html'
    fields = ['name', 'summary','capacity', 'show_comments', 'picture']
    context_object_name = 'group'


class SearchResultListView(ListView):
    model = Squad
    context_object_name = 'search_results'
    template_name = 'squads/search_results.html'
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        return Squad.objects.filter(
            Q(name__icontains=query) | Q(eng_title__icontains=query) | Q(summary__icontains=query)
        )

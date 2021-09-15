from django.db import connection, models
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import DetailView, UpdateView
from django.core.paginator import Paginator

from .models import Post, Category
from .forms import CommentForm

import datetime


def home(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        if posts.count() > 5:
            paginator = Paginator(posts, 12)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        else:
            page_obj = posts
        
        categories = Category.objects.all()
        a_list = Post.objects.filter(created_at__year=2021)
        context = {
            'monthly_archive' : a_list,
            'posts': posts,
            'categories' : categories,
            'page_obj': page_obj,
        }
    return render(request, 'blog/home.html', context)




def year_archive(request, year):
    a_list = Post.objects.filter(created_at__year=year)
    context = {
            'year' : year,
            'yearly_archive' : a_list,
        }
    return render(request, 'blog/year_archive.html', context)

def month_archive(request, year, month):
    a_list = Post.objects.filter(created_at__year=year).filter(created_at__month=month)
    datetime_object = datetime.datetime.strptime(f'{month}', "%m")
    month_name = datetime_object.strftime("%b")
    context = {
        'year' : year,
        'month': month,
        'month_archive' : a_list,
        'month_name' : month_name,
    }
    return render(request, 'blog/month_archive.html', context)


def category_posts(request, eng_title):
    posts_in_category = Post.objects.filter(category__eng_title=eng_title)
    cat_title = posts_in_category[0].category
    context = {
        'category_posts': posts_in_category,
        'cat_title' : cat_title
    }
    return render(request, 'blog/category_posts.html', context)



def post_detail(request, slug):
    template_name = 'blog/post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(is_active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {'post': post,
                'comments': comments,
                'new_comment': new_comment,
                'comment_form': comment_form}

    return render(request, template_name, context)



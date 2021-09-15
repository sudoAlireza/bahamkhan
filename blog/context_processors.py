from .models import Category, Post, Comment


def sections_processor(request):
    categories = Category.objects.all
    a_list = Post.objects.filter(created_at__year=2021)
    last_three_posts=Post.objects.all()[:2]

    return {'categories': categories, 'monthly_archive' : a_list, 'last_three_posts':last_three_posts}

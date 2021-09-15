from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog_home'),
    path('archive/<int:year>/', views.year_archive, name='year-archive'),
    path('archive/<int:year>/<int:month>/', views.month_archive, name='month-archive'),
    path('category/<eng_title>/', views.category_posts, name='category-posts'),
    path('posts/<slug:slug>/', views.post_detail, name='post-details'),

]

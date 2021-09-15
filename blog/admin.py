from django.contrib import admin
from django.db import models
from blog.models import Post, Category, Comment
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin




class CommentInline(admin.StackedInline):
    model = Comment
    classes = ['collapse']
    fieldsets = [
    ('Start Expanded', {
    'fields': ['name', 'email', 'content'],
    'classes': ['collapse in',]
    })
]



class CommentAdmin(admin.ModelAdmin):
    def jalali_date(self, obj):
        return obj.created_at.strftime("%d %b %Y %H:%M")
    jalali_date.admin_order_field = 'created_at'
    jalali_date.short_description = 'تاریخ ایجاد'
    list_display = ('name', 'content', 'post', 'jalali_date', 'is_active')
    list_filter = (
        ('created_at', JDateFieldListFilter),
        'is_active'
        )
    search_fields = ('name', 'email', 'content')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_active=True)



class PostAdmin(admin.ModelAdmin):
    def jalali_date(self, obj):
        return obj.created_at.strftime("%d %b %Y %H:%M")
    jalali_date.admin_order_field = 'created_at'
    jalali_date.short_description = 'تاریخ ایجاد'    

    
    list_display = ('title', 'author' ,'jalali_date' ,'category', 'is_published')
    list_filter = ('category', 'created_at', 'is_publlished', 'author')
    search_fields = ('title', 'content')
    # exclude = ('author',)
    actions = ['publish_drafts']
    inlines = [
        CommentInline,
    ]


    list_filter = (
        ('created_at', JDateFieldListFilter),
        ('updated_at', JDateFieldListFilter),
        ('published_at', JDateFieldListFilter),
    )
    # exclude = ('author',)
    # pass
    # fields = [
    #     'title',
    #     'content',
    #     'category',
    #     'created_at',
    #     'published_at',
    #     'author',
    #     'is_published',

    # ]

    def publish_drafts(self, request, queryset):
        queryset.update(is_published=True)


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            kwargs['initial'] = request.user.id
        return super(PostAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'eng_title')

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)

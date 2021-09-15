from django.db import models
from django.utils import timezone
from django.conf import settings
from django_jalali.db import models as jmodels
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField

from django.urls import reverse
from django.contrib.auth import get_user_model

from django.templatetags.static import static



class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان دسته‌بندی")
    eng_title = models.CharField(max_length=50, verbose_name="نامک دسته‌بندی", null=True, blank=True)

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/category/{self.eng_title}/"


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان پست")
    slug = models.SlugField(max_length=255)
    content = RichTextUploadingField(verbose_name="محتوای پست")
    category = models.ForeignKey(Category, verbose_name="انتخاب دسته‌بندی پست", on_delete=models.CASCADE)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='نویسنده'
    )
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="ایجاد شده در تاریخ")
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name="ویرایش شده در تاریخ")
    is_published = models.BooleanField(default= False, verbose_name="وضعیت انتشار")
    published_at = jmodels.jDateTimeField(null=True, blank=True, editable=False, verbose_name="منتشر شده در تاریخ")
    picture = models.ImageField(upload_to = 'blog_pics', null=True, blank=True)
    # post_tag = models.ManyToManyField(PostTag, null=True)

    def save(self, *args, **kwargs):
        self.slug = self.slug.replace(' ', '-')
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = "پست"
        verbose_name_plural = "پست‌ها"
        ordering = ["-created_at"]



    def publish(self):
        self.is_published = True
        self.published_at = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-details', kwargs={'slug': self.slug})

    @property
    def get_picture(self):
        return self.picture.url if self.picture else static('img/default-group-profile-picture.png')



class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=254, blank=False)
    content = models.TextField(max_length=500, blank=False)
    is_active = models.BooleanField(default=False, verbose_name='تایید شده')
    created_at = jmodels.jDateTimeField(auto_now_add=True, null=True, blank=True, editable=False, verbose_name='تاریخ ارسال')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت‌ها'


    def __str__(self):
        return f'کامنت {self.content} توسط کاربر {self.name}'

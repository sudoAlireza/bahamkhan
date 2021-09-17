from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from PIL import Image
from django.db.models.deletion import SET
from django.urls import reverse
from django.utils import timezone
from django.template.defaultfilters import slugify
from profiles.models import Profile
from django.templatetags.static import static

from easy_thumbnails.fields import ThumbnailerImageField
from django_jalali.db import models as jmodels

import uuid


class Squad(models.Model):
    name = models.CharField(max_length=50, verbose_name='اسم گروه')
    eng_title = models.CharField(max_length=100, unique=True, verbose_name='تایتل انگلیسی گروه', help_text='این قراره آدرس گروهتون باشه: \n bahamkhan.ir/group/example')
    slug = models.SlugField(null=False, unique=True)
    members = models.ManyToManyField(Profile,
                                     through='Membership',
                                     blank=True)
    summary = models.TextField(
        'توضیحات گروه',
        max_length=255,
        help_text='خلاصه اهداف گروه و کارهایی که قصد دارید تو گروه بکنید رو اینجا بنویسید.')
    date_created = jmodels.jDateTimeField(auto_now_add=True)
    MEMBERS_NUMBER = [
        (2, 'فقط ۲ نفر'),
        (5, '۳ تا ۵ نفر'),
        (10, '۵ تا ۱۰ نفر'),
    ]
    capacity = models.IntegerField(choices=MEMBERS_NUMBER, null = False, verbose_name='حداکثر ظرفیت گروه')
    creator = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    picture = ThumbnailerImageField(upload_to='groups_pictures', null=True, blank=True)
    show_comments = models.BooleanField(default=True, verbose_name='نمایش کامنت‌های برای کاربران غیر عضو')

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.name

    

    
    def save(self, *args, **kwargs):
        # instance = super(Squad, self).save(*args, **kwargs)
        # image = Image.open(instance.picture.path)
        # image.save(instance.picture.path,quality=20,optimize=True)
        
        if self.eng_title.isascii():
            self.slug = slugify(self.eng_title)
        elif not self.eng_title.isascii():
            self.slug = str(uuid.uuid4())
            self.eng_title = self.slug
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('group_detail', kwargs={'slug': self.slug})


    @property
    def get_picture(self):
        return self.picture.url if self.picture else static('img/default-group-profile-picture.png')


class Membership(models.Model):
    group = models.ForeignKey(Squad, on_delete=models.CASCADE)
    members = models.ForeignKey(Profile, on_delete=models.CASCADE)
    joining_date = jmodels.jDateTimeField(auto_now_add=True, null=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f'عضویت {self.members} در {self.group}'


    @property
    def approve_user(self):
        self.is_approved = True
        self.save()

    def remove_request(self):
        self.delete()

class Comment(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    group = models.ForeignKey(Squad, on_delete=models.CASCADE)
    pub_date = jmodels.jDateTimeField(auto_now_add=True)
    body = models.TextField(max_length=300,
                            help_text='درباره کارهایی که کردید بنویسید',
                            verbose_name='گزارش فعالیت')

    def __str__(self):
        return f'{self.author} در گروه {self.group} نوشته است'

    # def get_absolute_url(self):
    #     return reverse('reading:group-detail', kwargs={'slug' : self.group.slug})

    class Meta:
        ordering = ['-pub_date']


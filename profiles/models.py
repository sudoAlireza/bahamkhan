from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import gettext as _
from easy_thumbnails.fields import ThumbnailerImageField

from django.templatetags.static import static

class Profile(models.Model):
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_OTHER = 3
    GENDER_CHOICES = [
        (GENDER_MALE, _("مرد")),
        (GENDER_FEMALE, _("زن")),
        (GENDER_OTHER, ("نمی‌خواهم اشاره کنم")),
    ]

    user = models.OneToOneField(get_user_model(),
        related_name="profile",
        on_delete=models.CASCADE,
        editable=False,
        verbose_name='نام کاربری'
    )
    avatar = ThumbnailerImageField(upload_to="profile_pictures/",
        null=True,
        blank=True,
        verbose_name='آواتار'
    )
    birthday = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True, verbose_name='جنسیت')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True)

    class Meta:
        verbose_name = _('پروفایل')
        verbose_name_plural = _('پروفایل‌ها')


    def __str__(self):
        return self.user.username


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        return super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('profile_details', args=[str(self.slug)])

    @property
    def get_avatar(self):
        return self.avatar.url if self.avatar else static('img/default-user-profile-picture.png')
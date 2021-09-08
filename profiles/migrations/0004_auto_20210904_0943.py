# Generated by Django 3.2.7 on 2021-09-04 05:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0003_alter_profile_gender'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'پروفایل', 'verbose_name_plural': 'پروفایل\u200cها'},
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures', verbose_name='آواتار'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='birthday',
            field=models.DateField(blank=True, null=True, verbose_name='تاریخ تولد'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'مرد'), (2, 'زن'), (3, 'نمی\u200cخواهم اشاره کنم')], null=True, verbose_name='جنسیت'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='slug',
            field=models.SlugField(editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='نام کاربری'),
        ),
    ]
# Generated by Django 3.2.7 on 2021-09-04 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_profile_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'مرد'), (2, 'زن'), (3, 'نمی\u200cخواهم اشاره کنم')], null=True),
        ),
    ]
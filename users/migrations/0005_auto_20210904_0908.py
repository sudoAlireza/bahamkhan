# Generated by Django 3.2.7 on 2021-09-04 04:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_customuser_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='age',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='profile_picture',
        ),
    ]

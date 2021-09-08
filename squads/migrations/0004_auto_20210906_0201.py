# Generated by Django 3.2.7 on 2021-09-05 21:31

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('squads', '0003_alter_squad_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='pub_date',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='joining_date',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='squad',
            name='date_created',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True),
        ),
    ]
# Generated by Django 3.2.7 on 2021-09-05 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('squads', '0002_auto_20210905_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='squad',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='groups_pictures'),
        ),
    ]

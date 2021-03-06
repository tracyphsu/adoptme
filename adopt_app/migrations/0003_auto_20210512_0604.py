# Generated by Django 2.2 on 2021-05-12 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adopt_app', '0002_auto_20210511_0356'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pet',
            name='adopted',
        ),
        migrations.RemoveField(
            model_name='pet',
            name='user_fav',
        ),
        migrations.AddField(
            model_name='pet',
            name='user_fav',
            field=models.ManyToManyField(related_name='fav_pets', to='adopt_app.User'),
        ),
    ]

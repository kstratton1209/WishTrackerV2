# Generated by Django 2.2.4 on 2020-07-23 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_auto_20200723_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishes',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]

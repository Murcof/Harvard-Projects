# Generated by Django 3.1.2 on 2021-07-04 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_auto_20210630_0054'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='userfollowing',
            constraint=models.UniqueConstraint(fields=('user_id', 'following_user_id'), name='following'),
        ),
    ]

# Generated by Django 2.2.16 on 2021-11-28 14:18

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0008_auto_20211128_1716'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together={('author', 'user')},
        ),
    ]

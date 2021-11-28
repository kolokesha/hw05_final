# Generated by Django 2.2.16 on 2021-11-28 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_auto_20211128_1759'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='follow_unique',
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('author', 'user'), name='super_const'),
        ),
    ]

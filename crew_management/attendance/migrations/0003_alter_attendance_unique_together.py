# Generated by Django 5.1.2 on 2024-11-23 20:07

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together={('user', 'date')},
        ),
    ]

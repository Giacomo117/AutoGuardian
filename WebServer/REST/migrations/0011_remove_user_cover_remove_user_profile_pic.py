# Generated by Django 5.0.2 on 2024-02-12 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('REST', '0010_user_cover'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='cover',
        ),
        migrations.RemoveField(
            model_name='user',
            name='profile_pic',
        ),
    ]

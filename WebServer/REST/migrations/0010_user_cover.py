# Generated by Django 5.0.2 on 2024-02-12 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('REST', '0009_alter_user_contacts'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cover',
            field=models.ImageField(blank=True, upload_to='covers/'),
        ),
    ]

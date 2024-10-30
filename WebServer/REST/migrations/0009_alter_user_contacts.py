# Generated by Django 5.0.2 on 2024-02-12 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('REST', '0008_user_contacts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='contacts',
            field=models.ManyToManyField(related_name='alert_contacts', to='REST.contact'),
        ),
    ]

# Generated by Django 5.0.2 on 2024-02-12 21:31

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('REST', '0013_alter_vehicle_last_update'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='last_update',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
    ]

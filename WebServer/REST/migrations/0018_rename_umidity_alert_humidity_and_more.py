# Generated by Django 5.0.2 on 2024-02-13 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('REST', '0017_alter_alert_s_alter_alert_t_alter_alert_u'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alert',
            old_name='umidity',
            new_name='humidity',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='umidity',
            new_name='humidity',
        ),
        migrations.AlterField(
            model_name='alert',
            name='s',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='alert',
            name='t',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='alert',
            name='u',
            field=models.BooleanField(default=0),
        ),
    ]

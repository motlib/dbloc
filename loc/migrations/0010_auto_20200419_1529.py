# Generated by Django 3.0.5 on 2020-04-19 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loc', '0009_teleport_target_building'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teleport',
            old_name='target_building',
            new_name='dest_building',
        ),
    ]

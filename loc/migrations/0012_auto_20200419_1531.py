# Generated by Django 3.0.5 on 2020-04-19 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loc', '0011_teleport_dest_floor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teleport',
            name='dest_building',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='loc.Building'),
        ),
        migrations.AlterField(
            model_name='teleport',
            name='dest_floor',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='loc.Floor'),
        ),
    ]

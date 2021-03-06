# Generated by Django 3.0.5 on 2020-05-22 07:39

import dbloc.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dbloc', '0004_auto_20200425_1110'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='plan',
            name='unique_level',
        ),
        migrations.AlterField(
            model_name='plan',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dbloc.Plan'),
        ),
        migrations.AlterField(
            model_name='teleport',
            name='x',
            field=models.FloatField(default=0.0, validators=[dbloc.models.validate_coord]),
        ),
        migrations.AlterField(
            model_name='teleport',
            name='y',
            field=models.FloatField(default=0.0, validators=[dbloc.models.validate_coord]),
        ),
    ]

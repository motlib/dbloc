# Generated by Django 3.0.5 on 2020-05-22 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbloc', '0005_auto_20200522_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='full_name',
            field=models.CharField(default='', max_length=2000),
        ),
    ]

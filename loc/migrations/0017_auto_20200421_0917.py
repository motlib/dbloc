# Generated by Django 3.0.5 on 2020-04-21 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loc', '0016_auto_20200421_0904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='address',
            field=models.TextField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='building',
            name='description',
            field=models.TextField(blank=True, default='', max_length=2000),
        ),
        migrations.AlterField(
            model_name='building',
            name='url',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='site',
            name='address',
            field=models.TextField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='site',
            name='description',
            field=models.TextField(blank=True, default='', max_length=2000),
        ),
        migrations.AlterField(
            model_name='site',
            name='url',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
    ]

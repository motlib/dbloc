# Generated by Django 3.0.5 on 2020-04-25 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loc', '0003_auto_20200424_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='level',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='url',
            field=models.URLField(blank=True, default='', max_length=1000),
        ),
    ]
# Generated by Django 3.0.4 on 2020-04-22 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20200411_2313'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useravailable',
            name='items',
        ),
        migrations.AddField(
            model_name='useravailable',
            name='items',
            field=models.ManyToManyField(to='home.VehicleAvailable'),
        ),
    ]
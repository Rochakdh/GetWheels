# Generated by Django 3.1.3 on 2021-02-22 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_auto_20210222_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicleavailable',
            name='terms',
            field=models.BooleanField(default=False),
        ),
    ]

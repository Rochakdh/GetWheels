# Generated by Django 3.1.3 on 2021-02-02 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_remove_vehicleavailable_vech_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemsordered',
            name='orderedfrom',
        ),
        migrations.RemoveField(
            model_name='useravailable',
            name='renter_details',
        ),
        migrations.DeleteModel(
            name='Renter',
        ),
    ]

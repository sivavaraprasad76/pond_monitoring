# Generated by Django 5.0.6 on 2024-07-10 18:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0008_alter_aeratorstatus_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aeratorstatus',
            name='phone_number',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='monitoring.user'),
        ),
    ]

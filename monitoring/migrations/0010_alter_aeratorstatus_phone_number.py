# Generated by Django 5.0.6 on 2024-07-10 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0009_alter_aeratorstatus_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aeratorstatus',
            name='phone_number',
            field=models.CharField(max_length=15),
        ),
    ]

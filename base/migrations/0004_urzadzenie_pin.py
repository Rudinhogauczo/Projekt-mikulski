# Generated by Django 5.0.4 on 2024-06-05 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_remove_uprawnieniauzytkownika_device_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='urzadzenie',
            name='pin',
            field=models.IntegerField(null=True),
        ),
    ]

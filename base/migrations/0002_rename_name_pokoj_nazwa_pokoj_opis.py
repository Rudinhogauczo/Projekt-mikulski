# Generated by Django 5.0.4 on 2024-06-04 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pokoj',
            old_name='name',
            new_name='nazwa',
        ),
        migrations.AddField(
            model_name='pokoj',
            name='opis',
            field=models.CharField(default='Brak', max_length=200),
        ),
    ]

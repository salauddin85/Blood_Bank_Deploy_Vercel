# Generated by Django 5.1 on 2024-10-04 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood_bank_releted', '0003_rename_blogpost_donorblogpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donorblogpost',
            name='image',
            field=models.ImageField(upload_to='blood_bank_releted/media/images'),
        ),
    ]
# Generated by Django 4.0.6 on 2023-02-16 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_resetpasswordtoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resetpasswordtoken',
            name='key',
            field=models.CharField(db_index=True, max_length=128, unique=True, verbose_name='Key'),
        ),
    ]
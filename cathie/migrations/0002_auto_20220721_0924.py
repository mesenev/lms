# Generated by Django 3.1.8 on 2022-07-21 09:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cathie', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catsaccount',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cats_account', to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]

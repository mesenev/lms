# Generated by Django 3.1.3 on 2021-04-25 03:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ('problem', '0002_auto_20210319_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='submit',
            name='submit_date',
            field=models.DateTimeField(auto_created=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

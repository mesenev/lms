# Generated by Django 4.0.6 on 2022-11-06 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0003_delete_lessonprogress'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessoncontent',
            name='is_teacher_only',
            field=models.BooleanField(default=False),
        ),
    ]

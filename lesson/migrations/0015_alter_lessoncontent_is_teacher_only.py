# Generated by Django 4.0.6 on 2023-05-02 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0014_alter_lessoncontent_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessoncontent',
            name='is_teacher_only',
            field=models.BooleanField(default=True),
        ),
    ]
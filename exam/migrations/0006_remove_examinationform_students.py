# Generated by Django 4.0.6 on 2023-03-03 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0005_examinationform_students'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examinationform',
            name='students',
        ),
    ]

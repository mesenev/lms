# Generated by Django 4.0.6 on 2023-03-04 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0004_alter_examsolution_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examinationform',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
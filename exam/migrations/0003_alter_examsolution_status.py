# Generated by Django 4.0.6 on 2023-03-01 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0002_remove_examsolution_answers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examsolution',
            name='status',
            field=models.CharField(choices=[('AWAIT VERIFICATION', 'await'), ('VERIFIED', 'verified')], default='AWAIT VERIFICATION', max_length=30),
        ),
    ]
# Generated by Django 4.0.6 on 2022-11-19 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0010_auto_20211111_0559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='cats_id',
            field=models.IntegerField(help_text='contest_id from cats (cid)', null=True),
        ),
    ]

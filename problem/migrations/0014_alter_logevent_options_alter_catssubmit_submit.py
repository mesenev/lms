# Generated by Django 4.0.6 on 2022-07-30 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0013_auto_20220111_0720'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='logevent',
            options={'ordering': ('-created_at', '-id')},
        ),
        migrations.AlterField(
            model_name='catssubmit',
            name='submit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cats_submit', to='problem.submit'),
        ),
    ]

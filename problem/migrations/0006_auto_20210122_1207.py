# Generated by Django 3.1.3 on 2021-01-22 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0005_auto_20210121_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='submit',
            name='cats_request_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='submit',
            name='status',
            field=models.CharField(choices=[('WA', 'Wrong answer'), ('OK', 'OK'), ('NP', 'NP'), ('RJ', 'Rejected'), ('CE', 'Compilation error'), ('LI', 'Linter error'), ('RE', 'Run-time error'), ('PE', 'Presentation error'), ('TL', 'Time limit exceeded'), ('IL', 'Idleness limit exceeded'), ('ML', 'Memory limit exceeded'), ('WL', 'Write limit exceeded'), ('SV', 'Security violation'), ('IS', 'Ignored submit'), ('AW', 'Awaiting manual verification'), ('MR', 'Rejected by manual verification'), ('BA', 'Banned')], default='NP', max_length=2),
        ),
    ]

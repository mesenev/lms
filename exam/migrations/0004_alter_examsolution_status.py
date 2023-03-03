from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0003_alter_examsolution_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examsolution',
            name='status',
            field=models.CharField(choices=[('await', 'AWAIT VERIFICATION'), ('verified', 'VERIFIED')], default='AWAIT VERIFICATION', max_length=30),
        ),
    ]

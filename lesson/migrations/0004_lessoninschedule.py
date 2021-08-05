# Generated by Django 3.1.8 on 2021-08-04 05:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0008_auto_20210511_0235'),
        ('lesson', '0003_delete_lessonprogress'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonInSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lesson.lesson')),
            ],
        ),
    ]

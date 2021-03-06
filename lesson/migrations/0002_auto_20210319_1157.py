# Generated by Django 3.1.3 on 2021-03-19 11:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lesson', '0001_initial'),
        ('course', '0002_auto_20210319_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonprogress',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lessoncontent',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lessoncontent',
            name='lesson',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='materials', to='lesson.lesson'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lessons', to='course.course'),
        ),
        migrations.AlterUniqueTogether(
            name='lessonprogress',
            unique_together={('lesson', 'user')},
        ),
    ]

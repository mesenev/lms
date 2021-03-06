# Generated by Django 3.1.3 on 2021-03-19 11:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseprogress',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='courselink',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course'),
        ),
        migrations.AddField(
            model_name='course',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author_for', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='staff',
            field=models.ManyToManyField(related_name='staff_for', through='users.CourseAssignTeacher', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(related_name='student_for', through='users.CourseAssignStudent', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='courseprogress',
            unique_together={('course', 'user')},
        ),
    ]

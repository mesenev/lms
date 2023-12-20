# Generated by Django 4.0.6 on 2023-12-04 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0012_remove_course_staff_remove_course_students'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_schedule', models.JSONField(default=dict, null=True)),
                ('points_for_passing', models.JSONField(default=dict, null=True)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='source_for', to='course.course')),
            ],
        ),
    ]

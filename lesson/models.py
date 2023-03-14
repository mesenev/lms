from django.contrib import admin
from django.db import models
import os
from course.models import Course
from users.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver


def attachment_file_name(instance, filename):
    return '/'.join(['attachments', filename])


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, related_name='lessons', null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    deadline = models.DateField(blank=True, null=True)
    is_hidden = models.BooleanField(default=True)
    scores = models.JSONField(null=False, default=dict)

    def __str__(self):
        return self.name


class LessonContent(models.Model):
    CONTENT_TYPE = [
        ('video', 'Video'),
        ('text', 'Text'),
        ('url', 'Url'),
    ]

    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, related_name='materials', null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=500)
    content_type = models.CharField(max_length=5, choices=CONTENT_TYPE, blank=True, null=True)
    content = models.TextField()
    is_teacher_only = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Attachment(models.Model):
    name = models.CharField(max_length=50)
    material = models.ForeignKey(LessonContent, on_delete=models.SET_NULL, related_name='attachments', null=True)
    file_url = models.FileField(upload_to=attachment_file_name)
    file_format = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.name


@receiver(pre_delete, sender=Attachment)
def delete_file_hook(sender, instance, using, **kwargs):
    instance.file_url.delete()


admin.site.register(Attachment)
admin.site.register(Lesson)
admin.site.register(LessonContent)

import datetime

from django.contrib import admin
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from course.models import Course
from users.models import User


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
    is_control_work = models.BooleanField(default=False)
    duration = models.IntegerField(blank=True, null=True)

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
    file_format = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name


@receiver(pre_delete, sender=Attachment)
def delete_file_hook(sender, instance, using, **kwargs):
    instance.file_url.delete()


class StudentControlWorkRelation(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=False, primary_key=True)
    control_work = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=False)
    start_time = models.DateTimeField(editable=False)
    end_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self.control_work.is_control_work and self.control_work.duration is not None:
            self.start_time = datetime.datetime.now()
            self.end_time = self.start_time + datetime.timedelta(seconds=self.control_work.duration)
        return super(StudentControlWorkRelation, self).save(*args, **kwargs)

    def __str__(self):
        return f"student {self.student} taking part in {self.control_work}"


admin.site.register(Attachment)
admin.site.register(Lesson)
admin.site.register(LessonContent)
admin.site.register(StudentControlWorkRelation)

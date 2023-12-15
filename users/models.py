import os
import random
from io import BytesIO

import binascii
from PIL import Image
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from django.db import models
from django.utils.translation import gettext_lazy as _


def content_file_name(instance, filename):
    filename = f"{instance.username}_avatar{os.path.splitext(filename)[0]}"
    return '/'.join(['avatars', 'originals', filename])


class StudyGroup(models.Model):
    study_group = models.CharField(max_length=20, unique=True, blank=True)

    def __str__(self):
        return self.study_group


class User(AbstractUser):
    study_group = models.ForeignKey(StudyGroup, on_delete=models.SET_NULL, null=True, blank=True)
    avatar_url = models.ImageField(upload_to=content_file_name, null=True, blank=True)
    thumbnail = models.ImageField(upload_to=f'avatars/thumbnail/', null=True, blank=True)
    __original_mode = None

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.__original_mode = self.avatar_url

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.avatar_url != self.__original_mode:
            self.__original_mode = self.avatar_url
            self.get_avatar()
        super(User, self).save(force_insert, force_update, *args, **kwargs)

    def get_avatar(self):
        if not self.avatar_url:
            return
        image = Image.open(self.avatar_url)
        image.thumbnail((49, 50), Image.ANTIALIAS)
        thumb_name, thumb_extension = os.path.splitext(self.avatar_url.name)
        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False

        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=True)
        temp_thumb.close()
        return True


class GroupAssignStudent(models.Model):
    group = models.ForeignKey('group.CourseGroup', on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, related_name='assigns', on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"user {self.user} on group {self.group} as student"

    class Meta:
        constraints = [models.UniqueConstraint(fields=['group', 'user'], name='only_one_assignment_student')]


class GroupAssignTeacher(models.Model):
    group = models.ForeignKey("group.CourseGroup", on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, related_name='assigns_as_teacher', on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"user {self.user} on group {self.group} as teacher"

    class Meta:
        constraints = [models.UniqueConstraint(fields=['group', 'user'], name='only_one_assignment_teacher')]


class ResetPasswordToken(models.Model):
    class Meta:
        verbose_name = _("Password Reset Token")
        verbose_name_plural = _("Password Reset Tokens")

    @staticmethod
    def generate_token(min_length=32, max_length=128):
        length = random.randint(min_length, max_length)
        return binascii.hexlify(
            os.urandom(max_length)
        ).decode()[0:length]

    id = models.AutoField(
        primary_key=True
    )

    user = models.ForeignKey(
        User,
        related_name='password_reset_tokens',
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    key = models.CharField(
        _("Key"),
        max_length=128,
        db_index=True,
        unique=True
    )

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_token()
        return super(ResetPasswordToken, self).save(*args, **kwargs)

    def __str__(self):
        return "Password reset token for user {user}".format(user=self.user)


admin.site.register(ResetPasswordToken)
admin.site.register(StudyGroup)
admin.site.register(GroupAssignStudent)
admin.site.register(GroupAssignTeacher)

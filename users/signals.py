from django.db.models.signals import post_save
from django.dispatch import receiver

from celery_app.tasks import send_email
from users.models import ResetPasswordToken


@receiver(post_save, sender=ResetPasswordToken)
def password_reset_token_created(sender, instance, created, *args, **kwargs):
    send_email.delay(instance.key, instance.user.email, instance.request.build_absolute_uri('/'))

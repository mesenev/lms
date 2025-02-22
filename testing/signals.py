from django.db.models.signals import post_save
from django.dispatch import receiver
from testing.models import TestingSubmit, TestingQueue

@receiver(post_save, sender=TestingSubmit)
def add_to_testing_queue(sender, instance, created, **kwargs):
    if created:
        TestingQueue.objects.create(submit=instance)
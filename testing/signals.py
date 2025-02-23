from django.db.models.signals import post_save
from django.dispatch import receiver
from testing.models import TestingSubmit, TestingQueue
from testing.utils.validation_utils import validate_code

@receiver(post_save, sender=TestingSubmit)
def add_to_testing_queue(sender, instance, created, **kwargs):
    if created:
        # Проверяем код перед добавлением в очередь
        if validate_code(instance.content.read().decode('utf-8'), instance.problem.language):
            TestingQueue.objects.create(submit=instance)
        else:
            instance.status = 'CE'  # Compilation Error
            instance.save()
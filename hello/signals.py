from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Task


@receiver(pre_save, sender=Task)
def notify_status_change(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_instance = Task.objects.get(pk=instance.pk)
    except Task.DoesNotExist:
        return
    if old_instance.status != instance.status:
        owner = instance.owner
        if owner and owner.email:
            send_mail(
                subject=f'Task "{instance.title}" status changed',
                message=f'The status of your task "{instance.title}" was changed from {old_instance.status} to {instance.status}.',
                from_email=None,
                recipient_list=[owner.email],
                fail_silently=False,
            )

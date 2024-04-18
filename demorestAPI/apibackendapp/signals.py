from django.db.models.signals import post_save
from django.dispatch import receiver
from  AppEcommerce.models import  CustomUser
from .tasks import send_welcome_email


@receiver(post_save, sender=CustomUser)
def send_welcome_emails(sender, instance, created, **kwargs):
    if created:
        send_welcome_email(instance.username, instance.email, instance.role)

# @receiver(post_save, sender=CustomUser)
# def setup_periodic_tasks():
#     send_cart_notification.apply_async(countdown=300, repeat=300, retry=False)
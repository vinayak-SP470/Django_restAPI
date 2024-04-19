from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from  AppEcommerce.models import  CustomUser
from datetime import datetime, timedelta

@shared_task
def send_welcome_email(username, email, role):

    subject = 'Welcome to Ecommerce'
    message = f"Hello {username},\n\nWelcome to our platform! We're excited to have you as a {role}.\n\nThank you!"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

@shared_task
def setup_periodic_tasks():

    customers_with_items = CustomUser.objects.filter(cart__isnull=False).distinct()
    for customer in customers_with_items:
        subject = 'Reminder: Items in Your Cart'
        message = f"Hello {customer.username},\n\nYou have items in your cart. Don't miss out, check them out now!!!\n\nThank you for using our platform."

        send_mail(subject, message, settings.EMAIL_HOST_USER, [customer.email])

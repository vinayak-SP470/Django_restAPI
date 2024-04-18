
from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demorestAPI.settings')
app = Celery('demorestAPI')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'send-email-every-60-seconds': {
        'task': 'apibackendapp.tasks.setup_periodic_tasks',
        'schedule': timedelta(seconds=60),
    },
}
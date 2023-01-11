import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bulletin.settings')

app = Celery('bulletin')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_monday_news': {
        'task': 'post_app.tasks.monday_post',
        'schedule': 30,
            #crontab(hour=8, minute=0, day_of_week='monday'),
        'args': (),
    },
}
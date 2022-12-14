from __future__ import absolute_import

import os
import sys

from celery import Celery
from django.conf import settings
import django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticket_sales.settings')
# os.environ.setdefault('DJANGO_CONFIGURATION', 'Local')
# todo: you should change -local- maybe in upper line

django.setup()
app = Celery('ticket_sales')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings',)

# Load task modules from all registered Django apps.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

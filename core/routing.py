from accounts.models import Notifications
from django.urls import path

from .consumers import *


ws_patterns = [
    path('api/v1/ws/notifications/',NotifyConsumer.as_asgi())
]
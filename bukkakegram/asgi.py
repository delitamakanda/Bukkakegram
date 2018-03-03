import os
import channels.asgi
from django import settings

if settings.DEBUG
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bukkakegram.settings")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bukkakegram.settings_production")
    
channel_layer = channels.asgi.get_channel_layer()

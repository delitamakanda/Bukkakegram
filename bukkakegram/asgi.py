import os
import channels.asgi

from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bukkakegram.settings_production")

channel_layer = channels.asgi.get_channel_layer()
channel_layer = DjangoWhiteNoise(channel_layer)

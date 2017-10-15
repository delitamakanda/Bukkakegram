#inherits from standard local settings
from bukkakegram.settings import *

import dj_database_url

DATABASES['default'] = dj_database_url.config()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['.herokuapp.com', '*',]

DEBUG = config('DEBUG', cast=bool)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

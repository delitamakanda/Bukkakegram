#inherits from standard local settings
from bukkake.settings import *

import dj_database_url

DATABASES['default'] = dj_database_url.config()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['.herokuapp.com', '*',]

DEBUG = False

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# cloudinary config
cloudinary.config(
    cloud_name = os.environ.get('cloud_name'), # replace by your own cloud name
    api_key = os.environ.get('api_key'), # your api key
    api_secret = os.environ.get('api_secret'), # your api secret
)

web2: gunicorn --worker-class eventlet -w 1 --pythonpath bukkakegram bukkakegram.wsgi:application --log-file -
web: daphne bukkakegram.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2
worker: python3 manage.py runworker -v2
worker2: celery -A account worker -B -l info

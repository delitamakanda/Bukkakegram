web: gunicorn --worker-class eventlet -w 1 --pythonpath bukkakegram bukkakegram.wsgi:application --log-file -
web2: daphne bukkakegram.asgi:channel_layer --port $PORT --bind 0.0.0.0
worker: python3 manage.py runworker
worker2: celery -A account worker -B -l info

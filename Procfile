web: waitress-serve --port=$PORT bukkakegram.wsgi:application
web2: daphne bukkakegram.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2
worker: python3 manage.py runworker -v2
worker2: celery -A account worker -B -l info

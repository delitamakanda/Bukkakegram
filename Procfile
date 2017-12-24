web: waitress-serve --port=$PORT bukkakegram.wsgi:application
runworker: python3 manage.py runworker
ws: daphne --port $PORT bukkakegram.asgi:channel_layer 
worker: celery -A account worker -B -l info

# BukkakeGram
refactor of bukkakegram pinterest-clone (python 3 and Django 1.11)

# CirclCI: continuous integration
[![CircleCI](https://circleci.com/gh/delitamakanda/Bukkakegram.svg?style=svg)](https://circleci.com/gh/delitamakanda/Bukkakegram)

# Use virtualenv
```
sudo pip install virtualenv
```
```
virtualenv venv -p python3 //install venv in the repo
```
```
source venv/bin/activate
```
```
exit virtualenv deactivate venv
```

# Use demo on local
```
cd root-project
```
```
pip install
```
```
python3 manage.py runserver
```
```
go to http://127.0.0.1:8000/
```

# Install redis

```
src/redis-server
```

# Celery Worker

```
celery -A account worker -B -l info
```

## Demo
[Bukkakegram](https://bukkakegram.herokuapp.com/)

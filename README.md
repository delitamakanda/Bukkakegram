# BukkakeGram
codeschool exercise for django

# CirclCI
[![CircleCI](https://circleci.com/gh/delitamakanda/BukkakeGram/tree/master.svg?style=svg)](https://circleci.com/gh/delitamakanda/BukkakeGram/tree/master)

# Use virtualenv
1. sudo pip install virtualenv
2. virtualenv venv //install venv in the repo
3. source venv/bin/activate
4. exit virtualenv deactivate venv


# Use demo on local
1. cd root-project
2. pip install
3. python manage.py runserver
4. go to http://127.0.0.1:8000/

# Demo on Heroku
1. https://bukkakegram.herokuapp.com/ user = Delita, Jerome, Lisa
2. https://bukkakegram.herokuapp.com/directory

# Nota Bene
d = Bukkake.objects.get(pk=3)
d.delete() //sélectionne par un id

'python manage.py loaddata directory/fixtures/team.json //load data from a json file'

# Fix for heroku
[http://stackoverflow.com/questions/15128135/setting-debug-false-causes-500-error](http://stackoverflow.com/questions/15128135/setting-debug-false-causes-500-error)
## I had the same problem with whitenoise. python manage.py collectstatic fixed it
* https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/

# Flatpages
https://docs.djangoproject.com/fr/1.10/ref/contrib/flatpages/

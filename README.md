# BukkakeGram
refactor of bukkakegram pinterest-clone (python 2 and Django 1.10)

# CirclCI: continuous integration
[![CircleCI](https://circleci.com/gh/delitamakanda/BukkakeGramNew/tree/master.svg?style=svg)](https://circleci.com/gh/delitamakanda/BukkakeGramNew/tree/master)

# Use virtualenv
```
sudo pip install virtualenv
```
```
virtualenv venv //install venv in the repo
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
python manage.py runserver
```
```
go to http://127.0.0.1:8000/
```

# test in local
```
cloudinary.config(
    cloud_name = "<cloud_name>", # replace by your own cloud name
    api_key = "<api_key>", # your api key
    api_secret = "<api_secret>", # your api secret
)
```

# live site
[BukkakeGram](https://bukkakegram.herokuapp.com/)

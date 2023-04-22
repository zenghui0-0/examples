1, django-admin.py startproject try_django
2, settings.py -> ALLOWED_HOSTS = ["*"]
3, settings.py -> DATABASES = {}
4, mysql ->  create database TRY;
5, python manage.py migrate
6, python manage.py createsuperuser
7, python manage.py runserver 0.0.0.0:8000

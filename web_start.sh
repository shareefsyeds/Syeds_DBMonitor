python3 manage.py makemigrations &&
python3 manage.py migrate &&
python3 manage.py runserver 172.23.162.119:8000 > logs/django-web.log 2>&1 &
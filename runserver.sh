python manage.py loaddata ingredienttype && \
python manage.py loaddata ingredient && \
gunicorn --bind 0.0.0.0:8000 course_maker.wsgi
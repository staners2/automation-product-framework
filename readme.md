postgresql database

poetry run python manage.py 8000

poetry run python manage.py migrate
poetry run python manage.py migrate django_cron

python manage.py runcrons "product_app.cron.EventDaily.EventDaily"
python manage.py runcrons --force
python manage.py runcrons --silent

TODO:
- [ ] Подставлять разные сериализаторы в Swagger
- [ ] [Добавить проверку на уникальность обновляемых событий у каждого продукта](web/serializers/events/CreateEventsSerializer.py)


Запуск celery:
Worker: celery -A web.celery worker --loglevel=info -P eventlet

Планировщик: celery -A web.celery beat --loglevel=info

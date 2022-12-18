postgresql database

poetry run python manage.py 8000

poetry run python manage.py migrate
poetry run python manage.py migrate django_cron

python manage.py runcrons "product_app.cron.EventDaily.EventDaily"
python manage.py runcrons --force
python manage.py runcrons --silent
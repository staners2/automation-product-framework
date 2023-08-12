FROM harbor.eltc.ru/gitlab-ci/poetry:3.10-1.2.2

WORKDIR /app
COPY . .

RUN poetry install --only main
EXPOSE 8001

CMD poetry run python manage.py crontab add && poetry run gunicorn --workers 3 --bind 0.0.0.0:8001 web.wsgi:application


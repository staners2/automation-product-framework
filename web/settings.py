"""
Django settings for web project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

from dynaconf import Dynaconf

_settings = Dynaconf(load_dotenv=True, envvar_prefix=False)

# Celery settings
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"
CELERY_TIMEZONE = ""

# App settings
BOT_TOKEN = _settings.BOT_TOKEN

SAURON_URL = _settings.SAURON_URL
SAURON_CLIENT_SECRET = _settings.SAURON_CLIENT_SECRET

JIRABOT_USERNAME = _settings.JIRABOT_USERNAME
JIRABOT_PASSWORD = _settings.JIRABOT_PASSWORD

JIRA_URL = _settings.JIRA_URL
JIRA_USER = _settings.JIRA_USER
JIRA_PASSWORD = _settings.JIRA_PASSWORD

DATABASE_USER = _settings.DATABASE_USER
DATABASE_PASSWORD = _settings.DATABASE_PASSWORD
DATABASE_HOST = _settings.DATABASE_HOST
DATABASE_PORT = _settings.DATABASE_PORT

# Django settings
DJANGO_SETTINGS_MODULE = "web.settings"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-lv^q2fwo!0vjz9j(h-&%zwtew!&oyys=5^mx5(^7za6bh)$@q-"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Allow only json response
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_PARSER_CLASSES": ("rest_framework.parsers.JSONParser",),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'rest_framework.authentication.BasicAuthentication',
    # )
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "COERCE_DECIMAL_TO_STRING": False,  # Возвращает поля Decimal в API числом
}

# Django debug for docker
# if DEBUG:
# import socket  # only if you haven't already imported this

# hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
# INTERNAL_IPS = [ip[: ip.rfind('.')] + '.1' for ip in ips] + ['127.0.0.1', '10.0.2.2']

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "web.apps.ProductConfig",
    "background.apps.BackgroundConfig",
    "debug_toolbar",
    "django_extensions",  # для print sql query shell_plus
    # 'drf_yasg',  # swagger
    "django_celery_results",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # django debug
    # Для debug ответов json |
    "debug_toolbar_force.middleware.ForceDebugToolbarMiddleware",
]

ROOT_URLCONF = "web.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "web.wsgi.application"


# Password validationpython manage.py shell
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "ru"

USE_I18N = False

USE_L10N = False

USE_TZ = False

DATE_INPUT_FORMATS = ["%Y-%d-%m"]
# DATE_INPUT_FORMATS = ['%d-%m-%Y']
# DATE_FORMAT = ['%d-%m-%Y']


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

if DEBUG:
    # make all loggers use the console.
    # for logger in LOGGING['loggers']:
    #     LOGGING['loggers'][logger]['handlers'] = ['console']

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        },
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "myproject",
            "USER": f"{_settings.DATABASE_USER}",
            "PASSWORD": f"{_settings.DATABASE_PASSWORD}",
            "HOST": f"{_settings.DATABASE_HOST}",
            "PORT": f"{_settings.DATABASE_PORT}",
        },
    }

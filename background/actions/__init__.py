import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")
import django
django.setup()
import logging.config
logging.config.fileConfig("logging.conf")
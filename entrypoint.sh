echo 'Applying migrations...'
python manage.py wait_for_db --settings=config.settings.production
python manage.py migrate --settings=config.settings.production

export DJANGO_SETTINGS_MODULE=bilim_ai.settings
gunicorn bilim_ai.wsgi:application --bind 0.0.0.0:8000

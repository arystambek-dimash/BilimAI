export DJANGO_SETTINGS_MODULE=bilim_ai.settings

echo 'Applying migrations...'
python manage.py makemigrations
python manage.py migrate


python manage.py runsever
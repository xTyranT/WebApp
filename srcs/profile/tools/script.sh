#!/bin/bash

pip install --upgrade pip --root-user-action=ignore

if [ -f "/tmp/req.txt" ]; then
    pip install -r /tmp/req.txt --root-user-action=ignore
    rm -rf /tmp/req.txt #> /dev/null 2>&1
else
    echo "requirements already installed"
fi

python manage.py makemigrations api --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
# python manage.py runserver 0.0.0.0:$PROF_PORT || this is only for development
gunicorn --bind 0.0.0.0:$PROF_PORT user_profile.wsgi
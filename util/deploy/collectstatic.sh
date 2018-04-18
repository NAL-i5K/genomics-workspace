#!/bin/bash

PROJ_PATH="/usr/local/i5k"

cd $PROJ_PATH
source env/bin/activate
python manage.py collectstatic --noinput
deactivate


#!/bin/bash

LOCATION=`pwd`

cd ${LOCATION}
env | grep -E "(DB_|DIR)"

source ~/.bashrc
source ${LOCATION}/.envrc
APP_HOME/.venv/bin/uwsgi --ini ${LOCATION}/i5k.ini

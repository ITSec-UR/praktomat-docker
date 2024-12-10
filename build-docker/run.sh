#!/bin/sh

# Wait for database to be available
./wait-for-it.sh ${POSTGRES_HOST}:${POSTGRES_PORT}

# Dump environment variables (required for running checkers with cron)
env | egrep "^(PRAKTOMAT|COMPOSE_PROJECT_NAME|PATH)" > praktomat.env

# Start cron
sudo cron

# Apply migrations and run Praktomat
python3 Praktomat/src/manage-local.py migrate --noinput
python3 Praktomat/src/manage-local.py createsuperuser --username praktomat --no-input --email ${PRAKTOMAT_ADMIN}
sudo -E apache2ctl -DFOREGROUND
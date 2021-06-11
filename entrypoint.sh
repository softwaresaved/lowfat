#!/bin/bash

# Ensure database migrations are applied
python3 manage.py migrate
python3 manage.py collectstatic --no-input

exec $@

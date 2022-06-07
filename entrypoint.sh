#!/bin/bash

# Ensure database migrations are applied
python3 manage.py migrate

# Ensure staticfiles are available
python3 manage.py collectstatic --no-input

exec $@

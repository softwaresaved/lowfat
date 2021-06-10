#!/bin/bash

# Ensure database migrations are applied
python3 manage.py migrate

exec $@

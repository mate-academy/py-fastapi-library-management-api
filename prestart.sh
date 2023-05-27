#! /usr/bin/env bash

# Let the DB start
python ./main.py

# Run migrations
alembic upgrade head

## Create initial data in DB
#python /app/app/initial_data.py

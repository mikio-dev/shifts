#! /usr/bin/env bash

# Let the DB start
python ./app/check_db.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python ./app/load_init_data.py
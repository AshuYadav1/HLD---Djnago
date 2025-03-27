#!/bin/sh
set -e

# Run database migrations
python manage.py migrate

# Execute CMD
exec "$@"
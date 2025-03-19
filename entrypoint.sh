#!/bin/bash
set -e

alembic revision --autogenerate -m "Auto migration"
alembic upgrade head

exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
#!/bin/bash
set -e

exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
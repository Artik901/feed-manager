#!/bin/bash

set -e

cd /opt/feed-manager

source venv/bin/activate

exec gunicorn \
--workers 2 \
--timeout 120 \
--bind 127.0.0.1:8000 \
web:app
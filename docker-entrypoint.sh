#!/bin/bash
set -e

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:5000 --workers 2 server:app

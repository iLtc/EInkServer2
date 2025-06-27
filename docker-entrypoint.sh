#!/bin/bash
set -e

# Set timezone
export TZ=America/Los_Angeles
ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:5000 --workers 2 server:app

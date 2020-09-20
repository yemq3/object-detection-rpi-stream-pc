#!/bin/sh
gunicorn -k eventlet -b 0.0.0.0:9000 -w 1 wsgi:app

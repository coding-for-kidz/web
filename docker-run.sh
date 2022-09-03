#!/bin/sh
gunicorn --bind 0.0.0.0:5000 docker_run:app -w 3

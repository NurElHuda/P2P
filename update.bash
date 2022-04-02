#!/usr/bin/env bash

source venv/bin/activate
git pull
pip3 install -r requirements/local.txt
python3 manage.py migrate

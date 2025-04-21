#!/bin/bash
# Ensure the correct environment variables are used
export FLASK_APP=app.py
python -m flask run --host=0.0.0.0 --port=$PORT

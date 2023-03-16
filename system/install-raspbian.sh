#!/bin/sh
export PROJECT_HOME="/usr/src/venv/"
export WORKON_HOME="/usr/local/share/.virtualenvs"
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh

mkdir -p /usr/local/share/.virtualenvs
mkvirtualenv display
pip install -r ../src/display/requirements.txt

mkdir -p /etc/display
cp example.env /etc/display/display.env
cp display.service /lib/systemd/system/display.service
systemctl daemon-reload
systemctl enable display.service
systemctl start display
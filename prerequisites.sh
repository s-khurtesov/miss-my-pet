#!/bin/bash

if [[ $(/usr/bin/id -u) -ne 0 ]]; then
    echo "Launch as root to install required software"
    exit
fi

apt-get update -y

apt install -y python3
apt install -y python3-venv

python3 -m venv env && \
source env/bin/activate && \
python3 -m pip install -r requirements.txt

apt-get install -y mysql-server

exit $?

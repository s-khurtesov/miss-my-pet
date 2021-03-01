#!/bin/bash

# We need privileges to run mysql service
if [[ $(/usr/bin/id -u) -ne 0 ]]; then
    echo "Launch as root to get access to MySQL DB"
    exit
fi

# Trying to start mysql
service mysql start
if [ $? -ne 0 ]; then
    exit_code=$?
    echo "[ERROR] Couldn't start mysql service: ${exit_code}" >&2
    exit
fi
echo "[+] MySQL service started"


# Create DB used in Django project settings

DB_name=pet_mysql_db
DB_user=dbuser
DB_user_password=123

mysql -u root -e "CREATE DATABASE ${DB_name}";
if [ $? -ne 0 ]; then
    exit_code=$?
    echo "[ERROR] Couldn't create database ${DB_name}: ${exit_code}" >&2
    exit
fi
echo "[+] Database ${DB_name} created"

# Create user used in Django project settings
mysql -u root -e "CREATE USER ${DB_user}@'localhost' IDENTIFIED BY '${DB_user_password}'";
if [ $? -ne 0 ]; then
    exit_code=$?
    echo "[ERROR] Couldn't create mysql user ${DB_user}: ${exit_code}" >&2
    exit
fi
echo "[+] User ${DB_user} created"

# Grant privileges for new user
mysql -u root -e "GRANT ALL PRIVILEGES ON ${DB_name}. * TO ${DB_user}@'localhost'";
mysql -u root -e "FLUSH PRIVILEGES";


exit $?

#!/bin/bash

cd /kipnerter/puggy/
git pull --no-edit
cp /kipnerter/puggy/docs/* /var/www/html
cp /kipnerter/puggy/bin/* /kipnerter/bin
chown -R caddy:www-data /var/www/html
chmod 744 /var/www/html/*
chmod 744 /var/www/html/*/*
chmod 744 /var/www/html/*/*/*
echo Complete

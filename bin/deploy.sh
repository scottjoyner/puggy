cd /kipnerter/puggy/
git pull
cp /kipnerter/puggy/docs/* /var/www/html
chown -R caddy:www-data /var/www/html
chmod 744 /var/www/html/*
chmod 744 /var/www/html/*/*
chmod 744 /var/www/html/*/*/*

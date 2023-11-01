#!/bin/bash

# Define the log file location
LOG_FILE="/var/log/my_script.log"

{
    # Change to the required directory
    cd /kipnerter/puggy/ || exit 1

    # Pull the latest changes from the git repository
    git pull --no-edit

    # Copy the files to the appropriate locations
    cp /kipnerter/puggy/docs/* /var/www/html
    cp /kipnerter/puggy/bin/* /kipnerter/bin

    # Change the ownership of the files
    chown -R caddy:www-data /var/www/html

    # Set the appropriate permissions
    chmod 744 /var/www/html/*
    chmod 744 /var/www/html/*/*
    chmod 744 /var/www/html/*/*/*

    # Print completion message
    echo "Complete"

} >> "$LOG_FILE" 2>&1

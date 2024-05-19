#!/bin/bash
set -e

SITE_CONFIG=$1
SITE_NAME=$(basename "$SITE_CONFIG" .conf)

AVAILABLE="/etc/nginx/sites-available/$SITE_NAME.conf"
ENABLED="/etc/nginx/sites-enabled/$SITE_NAME.conf"

if [ ! -f "$AVAILABLE" ]; then
    echo "Error: $AVAILABLE does not exist."
    exit 1
fi

ln -sf "$AVAILABLE" "$ENABLED"
nginx -t && systemctl reload nginx


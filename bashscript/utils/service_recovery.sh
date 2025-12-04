#!/bin/bash
SERVICE=$1
[[ -z "$SERVICE" ]] && echo "Usage : $0 <service>" && exit 1

while true; do
    if ! systemctl is-active --quiet "$SERVICE"; then
        echo "Service $SERVICE is down. Attempting to restart..."
        systemctl restart "$SERVICE"
    fi
    sleep 5
done        
#!/bin/bash

THRESHOLD=85
USAGE=$(df / | awk 'NR==2 {print $5}' | tr -d '%')
if (( $USAGE > THRESHOLD )); then
    echo "Disk usage is at ${USAGE}%"
fi    
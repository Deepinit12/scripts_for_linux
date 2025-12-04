#!/bin/bash

set -e
HOST=$1
if [[ -z "$HOST"  ]]; then 
    echo "Usage: $0 <host>" 
    exit 1 
fi

echo "== Checking DNS =="
dig +short "$HOST" 

echo "== Traceroute =="
traceroute -I "$HOST"

echo "== MTU discovery/ Path MTU =="
ping -M do -s 1472 "$HOST" -c 1

echo "== Curl timing =="
curl -o /dev/null -s -w "DNS: %{time_namelookup}, Connect: %{time_connect}, TTFB: %{time_starttransfer}, Total: %{time_total}\n" "http://$HOST"
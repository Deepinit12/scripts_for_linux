#!/bin/bash

HOST=$1
[[ -z "$HOST" ]] && echo "Usage: $0 <host>" && exit 1
for p in $(seq 1 1024); do
    (echo >/dev/tcp/$HOST/$p) 2>/dev/null && echo "Port $p is open"
done
wait

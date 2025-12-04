#!/bin/bash
CMD=$1
shift
for host in "$@"; do
echo "== $host =="
ssh "$host" "$CMD"
done
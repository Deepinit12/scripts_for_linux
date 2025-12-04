#!/bin/bash
PID=$1
[[ -z "$PID" ]] && echo "Usage: $0 <pid>" && exit 1
pkill -TERM -P "$PID"
kill -TERM "$PID"
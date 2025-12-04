#!/bin/bash

# ========================================
# Auto Network Interface Watcher
# ========================================

IFACE=$1
LOG_FILE="/var/log/netwatch.log"

# Проверка аргумента
if [[ -z "$IFACE" ]]; then
    echo "Usage: $0 <network_interface>"
    exit 1
fi

# Проверка прав root
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root."
    exit 1
fi

# Проверка существования интерфейса
if ! ip link show "$IFACE" &>/dev/null; then
    echo "Interface $IFACE does not exist."
    exit 1
fi

echo "$(date): Starting network watcher for interface $IFACE" >> "$LOG_FILE"

# Основной цикл
while true; do
    if ! ip link show "$IFACE" | grep -q "state UP"; then
        echo "$(date): Interface $IFACE is down. Attempting to bring it up..." | tee -a "$LOG_FILE"
        ip link set "$IFACE" up
        if [[ $? -eq 0 ]]; then
            echo "$(date): Interface $IFACE successfully brought up." >> "$LOG_FILE"
        else
            echo "$(date): Failed to bring up interface $IFACE!" >> "$LOG_FILE"
        fi
    fi
    sleep 5
done
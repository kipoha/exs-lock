#!/bin/bash

if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root"
    exit 1
fi

rm -rf /usr/local/bin/exs-lock
rm -rf /opt/exs-lock

echo "Uninstallation complete!"

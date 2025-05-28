#!/bin/bash
# Make sure the script runs with super user privileges.
[ "$UID" -eq 0 ] || exec sudo bash "$0" "$@"
sudo ip link set can0 up type can bitrate 1000000
sudo ifconfig can0 txqueuelen 65536
sudo ifconfig can0 up
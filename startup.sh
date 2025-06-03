#!/bin/sh

cd $HOME/Vega/
./can.sh
python MQTT/control_subscriber.py
python MQTT/webcan_publisher.py
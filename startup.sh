#!/bin/sh

cd $HOME/Vega/
./can.sh
./mediamtx &
./RTSPpub.sh &
python MQTT/control_subscriber.py &
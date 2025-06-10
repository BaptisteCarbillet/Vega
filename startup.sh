#!/bin/sh

cd $HOME/Vega/
./can.sh
./mediamtx &
./RTSPpub.sh &
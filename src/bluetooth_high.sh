#!/bin/bash

TEST="2480MHz, Single channel, Non-hopping, Max power output"

printf "#############################################################################\nBeggining transmition: "
echo $TEST
sudo hcitool cmd 3f 14 00 50 01 00 09 00 00 #Transmittion start

echo "Transmitting"
sleep 120 #Run time

sudo hcitool cmd 08 1F #Stop transmitting
echo "Transmition stopped"
sudo hcitool cmd 03 03 #Rest bluetooth
echo "Bluetooth reset"


#!/bin/bash

TEST="2480MHz, Single channel, Non-hopping, Max power output"

printf "#############################################################################\nCtrl + C to terminate\nBeggining transmition: "
echo $TEST
sudo hcitool cmd 3f 14 00 50 01 00 09 00 00

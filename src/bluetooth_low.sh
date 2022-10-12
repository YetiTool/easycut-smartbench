#!/bin/bash

TEST="2402MHz, Single channel, Non-hopping, Max power output"

printf "#############################################################################\nCtrl + C to terminate\nBeggining transmition: "
echo $TEST
sudo hcitool cmd 3f 14 00 02 01 00 09 00 00

#!/bin/bash

TEST="5GHz 5755MHz 4000mW"

echo "Configuring test: "$TEST

sudo ./wl -i wlan0 down
sudo ./wl -i wlan0 frameburst 1 
sudo ./wl -i wlan0 ampdu 1
sudo ./wl -i wlan0 country ALL
sudo ./wl -i wlan0 bi 65000
sudo ./wl -i wlan0 phy_watchdog 0
sudo ./wl -i wlan0 mpc 0
sudo ./wl -i wlan0 txchain 1
sudo ./wl -i wlan0 mimo_bw_cap 1
sudo ./wl -i wlan0 band a
sudo ./wl -i wlan0 chanspec 157/40
sudo ./wl -i wlan0 5g_rate -h 0 -b 40
sudo ./wl -i wlan0 up
sudo ./wl -i wlan0 disassoc
sudo ./wl -i wlan0 phy_forcecal 1
sudo ./wl -i wlan0 scansuppress 1
sudo ./wl -i wlan0 txpwr1 -o -m 4000

echo "setup complete"

echo "Begining test: "$TEST

sudo ./wl -i wlan0 pkteng_start 00:11:22:33:44:55 tx 20 1500 0

sleep 5

echo "Stopping test"

sudo .w/ -i wlan0 pkteng_stop

echo "End of test: "$TEST

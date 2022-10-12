#!/bin/bash

TEST="2.4GHz 802.11b 1 mbs ch 1"

echo "Configuring test: "$TEST

sudo ./wl -i wlan0 out
sudo ./wl -i wlan0 down
sudo ./wl -i wlan0 frameburst 0
sudo ./wl -i wlan0 ampdu 1
sudo ./wl -i wlan0 country ALL
sudo ./wl -i wlan0 bi 65000
sudo ./wl -i wlan0 phy_watchdog 0
sudo ./wl -i wlan0 mpc 0
sudo ./wl -i wlan0 txchain 1
sudo ./wl -i wlan0 mimo_bw_cap 1
sudo ./wl -i wlan0 band b
sudo ./wl -i wlan0 chanspec -c 1 -b 2 -w 20 -s 0
sudo ./wl -i wlan0 2g_rate -r 1
sudo ./wl -i wlan0 up
sudo ./wl -i wlan0 disassoc
sudo ./wl -i wlan0 phy_forcecal 1
sudo ./wl -i wlan0 scansuppress 1
sudo ./wl -i wlan0 txpwr1 -o -q 70

echo "setup complete"

echo "Begining test: "$TEST

sudo ./wl -i wlan0 pkteng_start 00:11:22:33:44:55 tx 20 1500 0

sleep 10

echo "Stopping test"

sudo ./wl -i wlan0 pkteng_stop tx

echo "End of test: "$TEST

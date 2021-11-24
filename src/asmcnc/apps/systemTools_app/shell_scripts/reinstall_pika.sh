#!/bin/bash
pkill -f main.py
sleep 2

sudo python -m pip uninstall pika
sudo python -m pip install pika
sudo reboot
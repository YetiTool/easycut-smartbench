#!/bin/bash
pkill -f main.py
sleep 2

python -m pip uninstall pika
python -m pip install pika
reboot
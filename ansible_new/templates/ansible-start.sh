#!/bin/bash

export ANSIBLE_CONFIG="/home/pi/easycut-smartbench/ansible/ansible.cfg"
export ANSIBLE_INVENTORY="/home/pi/easycut-smartbench/ansible/hosts"
export ANSIBLE_LIBRARY="/home/pi/easycut-smartbench/ansible/"

# Ensure package lists are up to date
sudo apt-get update

sudo /usr/bin/ansible-galaxy \
	install \
	-r /home/pi/easycut-smartbench/ansible/requirements.yml

/usr/bin/ansible-playbook \
	-v \
	-l localhost \
	/home/pi/easycut-smartbench/ansible/init.yaml

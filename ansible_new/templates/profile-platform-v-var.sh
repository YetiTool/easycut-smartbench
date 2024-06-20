# shellcheck shell=sh

export SB_PLATFORM_VERSION=$(cd /home/pi/easycut-smartbench && git describe --always && cd)

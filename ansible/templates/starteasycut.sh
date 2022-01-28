#!/bin/bash
echo "start easycut"

# start the pigpio daemon
sudo pigpiod

# If easycut-smartbench directory doesn't exist, copy from backup (if available)
if [ ! -d "/home/pi/easycut-smartbench/" -a -d  "/home/pi/easycut-smartbench-backup" ]
then
        echo "no easycut folder found! copying files from backup folder"
        mkdir /home/pi/easycut-smartbench && cp -RT /home/pi/easycut-smartbench-backup /home/pi/easycut-smartbench
fi

if [ -f /home/pi/ZHEADTESTJIG.txt ]
then
        echo "running z head diagnostics"

        cd /home/pi/easycut-smartbench/src/
        exec python diagnostics.py
else
        cd /home/pi/easycut-smartbench/src/
        # execute python
        exec python main.py
        sleep 5

        # check if running
        echo "check main.py running"
        if ! ps ax | grep "[p]ython main.py"
        then
                echo "no main instance found - trying git reset"
                git reset --hard
                exec python main.py
                if ! ps ax | grep "[p]ython main.py"
                then
                        if [ -d  "/home/pi/easycut-smartbench-backup" ]
                        then
                                echo "force copy of easycut-smartbench-backup back into easycut-smartbench"
                                cp -RTf /home/pi/easycut-smartbench-backup /home/pi/easycut-smartbench
                                exec python main.py
                        fi
                fi
        fi
fi
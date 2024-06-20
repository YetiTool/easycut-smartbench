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

# Run all apps from src folder
cd /home/pi/easycut-smartbench/src/

if compgen -G "/home/pi/YETI_*_PROD_JIG.txt" > /dev/null; then

        if [ -f /home/pi/YETI_ZHEADQC_PROD_JIG.txt ]
        then
                echo "Running Z Head QC app"
                exec python z_head_qc_app.py

        elif [ -f /home/pi/YETI_ZHEADUPDOWN_PROD_JIG.txt ]
        then
                echo "Running Z Head Up Down app"
                exec python z_head_mechanics_app.py

        elif [ -f /home/pi/YETI_LBQC_PROD_JIG.txt ]
        then
                echo "Running LB QC app"
                exec python lower_beam_qc_app.py

        elif [ -f /home/pi/YETI_LBCAL_PROD_JIG.txt ]
        then
                echo "Running LB Calibration app"
                exec python lb_calibration_app.py

        fi

else
        
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
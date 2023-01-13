#!/bin/bash

BENCH_FULL=`cat /proc/cpuinfo | grep Serial | awk ' {print $3}'` 

if [[ $BENCH_FULL == 1* ]];
then 
	BENCH=`echo $BENCH_FULL | sed 's/^10*/4/'`
else
	BENCH=`echo $BENCH_FULL | sed 's/^0*//'`
fi

hostname ${BENCH}.yetitool.com
echo ${BENCH}.yetitool.com > /etc/hostname

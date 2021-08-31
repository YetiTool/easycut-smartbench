#   Linux Container docker file - called dockerfile in the src folder

#   YETI TOOL 
#	Docker Container 
#   Cross platform deployment to be run on any platform
#   Linux container, as this is what will run on the RASPBERRY PI

### RUN INSTRUCTIONS

# You will need to have Docker downloaded and have logged in, etc

# TO BUILD:
# cd to the /.../easycut-smartbench folder
# run this command in terminal / cmd:

# ~~~~~~~~~~~~~~               docker build -t yeti-001 .


# TO RUN, ONCE BUILD OK:
# run this command in terminal / cmd:

# ~~~~~~~~~~~~~~               docker run --rm -it yeti-001:latest /bin/bash

# NOTES:
#        -rm should remove the container after it has been run, so there aren't endless containers floating about



# Use a very light base image for the PI
### https://hub.docker.com/r/raspbian/stretch   
##             this is the most popular docker image by far by raspbian on the docker site
FROM pihole/pihole:v5.2.1
# PREVIOUS raspbian/stretch:041518
# ____ only for raspbian: RUN apt-get clean/update/dist-upgrade
# this previous has an warning? : 
# [Warning] The requested image's platform (linux/arm) does not match the detected host platform (linux/amd64) and no specific platform was requested


MAINTAINER Yeti Tool Support <support@yetitool.com>

## UNSURE IF WE NEED THIS, as base image not set:

# When we run the container, the command we choose is our main.py
## it's just the path to get there we need to confirm
# CMD ["/src/main.py"]


############################################################### 
#
#### Fetch and install all relevant dependencies and software
#
############################################################### 

# standard issue update && ...
RUN sudo apt-get update && apt-get install -y apt-transport-https

# STEPS to install basics
RUN apt-get install -y \
		git \
		unzip \
		wget \
 		bzip2 \
		cmake \
		curl 

# Install development tools:
#
# PREVOUSLY RECOMMENDED, TAKEN OUT FOR NOW
#
#RUN sudo apt-get install -y \
#		build-essential \
#		libreadline-gplv2-dev \
#		libncursesw5-dev \
#		libssl-dev \
#		libsqlite3-dev \
#		tk-dev \
#		libgdbm-dev \
#		libc6-dev \
#		libbz2-dev \
#		mesa-common-dev \
#		libgl1-mesa-dev \
#		xclip
		
		# NOTE: xclip not a deal breaker
		
		
# STEPS which will duplicate some of the above and the below, from 
## 
##### NEW ADDITIONS
# from https://github.com/YetiTool/console-raspi3b-plus-platform
##

RUN sudo apt-get install -y \
		libsdl2-dev \
		libsdl2-image-dev \
		libsdl2-mixer-dev \
		libsdl2-ttf-dev \
		pkg-config \
		libgl1-mesa-dev \
		libgles2-mesa-dev \
   		python-setuptools \
   		libgstreamer1.0-dev \
   		git-core \
		gstreamer1.0-plugins-{bad,base,good,ugly} \
   		gstreamer1.0-{omx,alsa} \
   		python-dev \
   		libmtdev-dev \
   		xclip \
   		xsel		
			
## 
##### NEW ADDITIONS
# from https://github.com/YetiTool/console-raspi3b-plus-platform
##		
RUN sudo apt-get -y install \
	python-serial
	
# STEPS TO install necessary system packages
# https://kivy.org/doc/stable/installation/installation-linux.html#dependencies-with-sdl2
# ________ those commented out are covered above

RUN sudo apt-get install -y \
#    libsdl2-dev \
#    libsdl2-image-dev \
#    libsdl2-mixer-dev \
#    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \      
    zlib1g-dev
#    libmtdev-dev
    
    # additional x1
 
# STEP to install Python 2.7 (not Python 3 for now)
## need to confirm what Python the base comes with
RUN sudo apt install -y \
		python-minimal \
		python-pip 

		# NOTE: taken out python 3 - just not needed yet
		#  	python3 \
		#	python3-pip
		#   python-minimal - THIS GIVES 2.7.16 not .17

# NOTE python2.7 \ # this gives python 2.7.16 not 2.7.17

## ADDITION TO RESOLVE SDL2 issue
# ________ those commented out are covered above

RUN sudo apt-get install -y \
#		python-setuptools \
		python-pygame \
		python-opengl \
		python-enchant \
#		python-dev \ 
		build-essential
#		libgl1-mesa-dev \
#		libgles2-mesa-dev \
#		python-pip \
#		libgstreamer1.0-dev
		
# STEP to install gstreamer for audio, video
# ________ these are mostly covered above, but not quite...
RUN sudo apt-get install -y \
	libgstreamer1.0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good

# 2 x RUN STEPS to install Kivy Dependencies:
# RUN python -m pip install docutils pygments 
# pypiwin32 kivy.deps.sdl2 kivy.deps.glew
# RUN python -m pip install kivy.deps.gstreamer

# STEP to install Cython
# NEW from https://github.com/YetiTool/console-raspi3b-plus-platform
RUN sudo pip install -U Cython==0.28.2

# RUN STEP to install Kivy
#### DON'T THINK installing Kivy in the python folder makes any difference
# Python folder path: 
RUN cd /usr/lib/python2.7
RUN python -m pip install kivy==1.11.1

# RUN STEP to install our serial 
RUN python -m pip install pyserial==3.4

# STEP to configure touchscreen to accept input
# SKIPPED FOR NOW
# NEW from https://github.com/YetiTool/console-raspi3b-plus-platform
# config touchscreen to accept input

# sudo nano ~/.kivy/config.ini
# ########### ... under [input] add
# mouse = mouse
# mtdev_%(name)s = probesysfs,provider=mtdev
# hid_%(name)s = probesysfs,provider=hidinput

# STEP to install splashscreen
# NEW from https://github.com/YetiTool/console-raspi3b-plus-platform
#
RUN sudo apt-get -y install plymouth plymouth-themes 
RUN sudo plymouth-set-default-theme -l
RUN sudo plymouth-set-default-theme -R spinfinity


# STEPS to silent boot - skipped for now


# STEPS to install and restart Ansible
# NEW from https://github.com/YetiTool/console-raspi3b-plus-platform
# NOTE: prepared to clone from here
RUN sudo apt -y install ansible

RUN sudo mkdir ~/media/
RUN sudo mkdir ~/media/usb
RUN sudo mkdir ~/router_ftp/ 
RUN cd root
RUN git clone https://github.com/YetiTool/console-raspi3b-plus-platform.git
RUN cd console-raspi3b-plus-platform/ansible
# RUN sudo ansible-playbook -v -i hosts -l localhost init.yaml
# RUN sudo systemctl restart ansible.service

# standard issue update && ...
RUN cd /
RUN sudo apt-get update

# Delete temporary zip files
#   RUN rm -irf *.zip *.gz


############################################################### 
#
#### Fetching latest code for use in our containerised running...
#
############################################################### 

# Setting some environment variables
#             SETTING PATH HERE LIKELY TO NEED TO BE ADJUSTED TO 
#             MATCH EXPECTATIONS OF THE WIDER SETUP (just HSTH working for now)
RUN sudo mkdir /easycut-smartbench/
ENV WORK /easycut-smartbench/

# Set up the python interpreter and it's path
## NOT SURE THIS IS RIGHT...

ENV PYTHONPATH=${WORK}:${PYTHONPATH}
ENV PYTHONPATH='/usr/bin/python2.7'

# set environment variables
ENV XDG_RUNTIME_DIR=$PATH:~/.cache/xdgr


# Copy easycut-smartbench files to convenient locations
COPY . ${WORK}
# 
# THIS COPY STEP IS A SHORTCUT TO GET THE RIGHT BRANCH
# see git clone, which needs branch specifics, below

# STEP to clone easycut-smartbench
# RUN cd && git clone https://github.com/YetiTool/easycut-smartbench.git

WORKDIR $WORK/src/


##############################################################################
#
###   WHAT THE CONTAINER DOES ONCE IT's LOADED
#
##############################################################################

# THIS RUNS THE CONSOLE APP ON CONTAINER ENTRY
# ENTRYPOINT python main.py
# REPLACE WITH THIS TO JUST ACCESS THE CONTAINER AT easycut-smartbench/src
CMD "ls" && /bin/bash


FROM resin/rpi-raspbian:buster

RUN apt-get update && apt-get install -y -q \
    build-essential \
    cython \
    git-core \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-alsa \
    gstreamer1.0-omx \
    libgl1-mesa-dev \
    libgles2-mesa-dev \
    libgstreamer1.0-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    pkg-config \
    python-dev \
    python-docutils \
    python-pip \
    python-setuptools \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

RUN pip install kivy==1.10.1


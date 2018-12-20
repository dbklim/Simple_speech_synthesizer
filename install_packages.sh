#!/bin/bash
apt-get -y update
add-apt-repository ppa:jonathonf/ffmpeg-3
apt-get -y update

# Установка пакетов Ubuntu
apt-get -y install python3.5 python3.5-dev python3-pip python3-tk ffmpeg libavcodec-extra

# Установка пакетов Python3
yes | pip3 install --upgrade pip
yes | pip3 install tkinter pydub simpleaudio

# Очистка кеша
apt-get -y autoremove
apt-get -y autoclean
apt-get -y clean



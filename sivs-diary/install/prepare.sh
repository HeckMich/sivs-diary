#!/bin/bash

# Variables
mkdir -p /home/ubuntu/
cd /home/ubuntu/

DIR="/home/ubuntu/sivs/"
sudo rm -rf $DIR
sudo mkdir -p $DIR
sudo chmod o+w $DIR
cd $DIR

wget https://sivs.untrace.it/sivs-diary.tar.xz
tar -xvf ./sivs-diary.tar.xz -C $DIR

chmod +x $DIR"sivs-diary/install/install.sh"
echo "Please continue with ./sivs/sivs-diary/install/install.sh"
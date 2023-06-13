#!/bin/bash

# Change to the directory where your script is located
cd /home/moxa/logs

# Execute your command
smbget -R -u smb://10.10.10.72/log -U CCP%Vdl@0184
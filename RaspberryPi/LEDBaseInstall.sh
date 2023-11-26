#!/bin/bash

#Defines for colored text output
SUCCESS=`tput setaf 2` 
FAILED=`tput setaf 1`
NONE=`tput sgr0`

#Input:
# $1: String to print
# $2: Color None/0: No Color 1: Green/Success 2: Red/Failed
Print()
{
  if [[ $2 -eq 0 ]]; then
       echo "${NONE}$1${NONE}"
  elif [[ $2 -eq 1 ]]; then
       echo "${SUCCESS}$1${NONE}"
  elif [[ $2 -eq 2 ]]; then
       echo "${FAILED}$1${NONE}"
  fi
}

# Static functions
CheckScriptPreconditions()
{
    if [[ $(id -u) -ne 0 ]]; then
        Print "ERROR: Must run script with sudo" 2
        exit 1
    else
        Print "Script run as sudo" 1
    fi

    if ping -c 1 google.com >> /dev/null 2>&1; then
        Print "Internet connection test success" 1
    else
        Print "ERROR: Device must be connected to the internet" 2
        exit 1
    fi
}

UpdateRepos()
{
    Print "Updating Apt Repositories" 1
    apt update
    
    Print "Upgrading Image" 1
    apt upgrade - y
}

InstallVim()
{
    Print "Installing VIM" 1
    apt -y install vim
}

LEDStripSetup()
{
    Print "Installing Python and NeoPixel tools" 1
 
    #For Debian 12 (Bookworm) in installation is quite ridiculous and requires a --break-system-packages flag!!
    apt install python3-pip
    apt install --upgrade python3-setuptools
    apt install python3.11-venv
    python -m venv env --system-site-packages
    source env/bin/activate
    
    sudo pip3 install --break-system-packages rpi_ws281x adafruit-circuitpython-neopixel

    Print "Creating /home/pi/NeoPixel.py" 1

cat > /home/pi/NeoPixel.py << EOF
# Usage: 
# sudo python NeoPixel.py <number_leds> <brightness> <red> <white> <green> <blue> <pin>
#
# brightness: 1.0 - 0
# red, white, green, blue: 0 - 255
# pin: 18 or 21
#
# Examples:
#sudo python NeoPixel.py 300 1.0 0 0 0 255 18 # Turns on blue GPIO18
#sudo python NeoPixel.py 300 1.0 255 0 0 0 21 # Turns on red GPIO21

import sys
import time
import board
import neopixel

# Parse command line arguments
pixel_count = int(sys.argv[1])
brightness = float(sys.argv[2])
color_values = tuple(map(int, sys.argv[3:7])) # RWGB

pin = int(sys.argv[7])

if pin == 21:
    pixel_pin = board.D21
else:
    pixel_pin = board.D18

pixels = neopixel.NeoPixel(pixel_pin, pixel_count, bpp=4, brightness=brightness)

pixels.fill(color_values)

EOF

    chmod +x /home/pi/NeoPixel.py

    Print "Disable audio to free up GPIO18 and GPIO21" 1
    sed -i 's/^dtparam=audio=on/dtparam=audio=off/' /boot/config.txt
}

ConfigureJournaldLogging()
{
    Print "Configuring journald logging..." 1

    sudo sed -i -e '/Storage=/c\Storage=persistent' /etc/systemd/journald.conf
  
    sudo sed -i -e '/Compress=/c\Compress=yes' /etc/systemd/journald.conf
    
    sudo sed -i -e '/SystemMaxUse=/c\SystemMaxUse=500M' /etc/systemd/journald.conf
  
    sudo sed -i -e '/ForwardToSyslog=/c\ForwardToSyslog=no' /etc/systemd/journald.conf
  
    sudo sed -i -e '/ForwardToKMsg=/c\ForwardToKMsg=no' /etc/systemd/journald.conf
    
    sudo sed -i -e '/ForwardToConsole=/c\ForwardToConsole=no' /etc/systemd/journald.conf
    
    sudo sed -i -e '/ForwardToWall=/c\ForwardToWall=no' /etc/systemd/journald.conf
}


# Main script

echo ""
Print "Starting Permanent Light installation script..." 1
Print "This script is designed to be rerunable so keep that in mind when adding anything new" 1
Print "Requires a reboot for all changes to take effect" 1
read -p "Press key to continue.. " -n1 -s
echo ""


CheckScriptPreconditions
UpdateRepos
InstallVim

InstallDotNet7

LEDStripSetup
ConfigureJournaldLogging

Print "Requires a reboot for all changes to take effect" 1
read -p "Press key to continue.. " -n1 -s
echo ""

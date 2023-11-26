# HomeLEDLighting
Code for a permanent home LED lighting system.

# Build

- Prerequisites:
    Install both WSL and Python 3 (Make sure to check the box to install python in your PATH during installation)
- Update Version:
    Update the version number in `Version.txt`
- Build:
    From a windows command line run `python BuildApplication.py`
    
# Install

- Copy Debian package: `./Build/led-service_x.x.x_all.deb`
- SCP the Debian package to Raspberry Pi and install with `sudo dpkg -i led-service_x.x.x_all.deb`
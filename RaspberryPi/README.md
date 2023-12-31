# Raspberry Pi README

### Image Creation w/ Raspberry Pi Imager

- Download the Raspberry Pi imager: https://www.raspberrypi.com/software/
- Select `Raspberry Pi OS (64-bit)`
In advanced options:
- Enable SSH (use password authentication)
- Set username:password:
- Configure Wireless LAN (WiFi) to connect to home WiFi
- Write the image to at least a 16GB uSD card

### Linux Setup

**WARNING:** If editing `LEDBaseInstall.sh` make sure your text editor is using Linux-style line endings `\n` or the script will not run. OR just don't open the install script at all. Notepad++ is a great tool that respects line endings

- scp `LEDBaseInstall.sh` to the Raspberry Pi (use a tool like WinSCP)
- ssh to Raspberry Pi using the username and password setup in the image creation
- Change the script permissions

    sudo chmod +x LEDBaseInstall.sh

- Run the script:

    sudo ./LEDBaseInstall.sh


### Image Info
After successful Linux Setup described above:
- Wifi is set to connect to home WiFi
- You'll need to manually find the WiFi IP on your network (look in router DHCP settings)


## Debian package

**Use the build script at the top level of this repo to build the application which calls this packaging script.**

#### Build

 - From a WSL command line, run `sudo ./BuildDebianPackages.sh x.x.x` where `x.x.x` is the version number
 - The output Debian package will be in the form: `led-service_x.x.x_all.deb`

#### Install

SCP the Debian package to Raspberry Pi and install with `sudo dpkg -i led-service_x.x.x_all.deb`
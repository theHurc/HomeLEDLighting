# Raspberry Pi README

### Image Creation w/ Raspberry Pi Imager

- Download the Raspberry Pi imager: https://www.raspberrypi.com/software/
- Select `Raspberry Pi OS (64-bit)` **64-bit critical for dot net 7.0**
In advanced options:
- Enable SSH (use password authentication)
- Set username:password: `pi:lightship!1`
- Configure Wireless LAN (WiFi) to connect to home WiFi
- Write the image to at least a 16GB uSD card

### Linux Setup

**WARNING:** If editing `LEDBaseInstall.sh` make sure your text editor is using Linux-style line endings `\n` or the script will not run. OR just don't open the install script at all. Notepad++ is a great tool that respects line endings

- scp `LEDBaseInstall.sh` to the Raspberry Pi (use a tool like WinSCP)
- ssh to Raspberry Pi `pi:lightship!1`
- Change the script permissions
`sudo chmod +x LEDBaseInstall.sh`
- Run the script:

    sudo ./LEDBaseInstall.sh


### Image Info
After successful Linux Setup described above:
- Wifi is set to connect to home WiFi
- You'll need to manually find the WiFi IP on your network (look in router DHCP settings)
- .NET 7.0 is installed and ready to go
- Added Python script to control LED strips `/home/pi/NeoPixel.py`. Check that file for usage info


## Building Debian package

From a WSL command line, run `sudo ./BuildDebianPackages.sh x.x.x` where `x.x.x` is the version number
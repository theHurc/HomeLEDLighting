#!/bin/bash

if [ $# -eq 0 ]
  then
    echo "Must enter a version number. No arguments supplied"
    exit 1
fi

# Assign the VERSION parameter to the first command line parameter
VERSION="$1"

echo "Removing Debian old Packages"

ALL_DEBIAN_PACKAGES="$(find . -maxdepth 4 -name '*.deb')"

for i in $ALL_DEBIAN_PACKAGES ; do
  echo "Removing .deb package $i"
  rm -rf $i
done

LED_SERVICE_PACKAGE_NAME="led-service"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
pushd $DIR

LED_SCRIPT_APPLICATION_PATH="../MovingPixel.py"

INSTALL_DIRECTORY="/opt/leds"
COMPANY="McKinley Ave"
COMPANY_CONTACT_INFO="jake.a.baldwin@gmail.com"

APP_VEHICLE_SERVER_OUTPUT_DEB_NAME="${LED_SERVICE_PACKAGE_NAME}_${VERSION}.deb"

if ! command -v fpm &> /dev/null; then
    echo "fpm is not installed. Install with:"
    echo "sudo apt update"
    echo "sudo apt install ruby ruby-dev rubygems build-essential -y"
    echo "sudo gem install --no-document fpm"
    exit 1
fi

echo "Packaging version: ${VERSION}"

fpm -s dir \
    -t deb \
    -a all \
    --vendor "$COMPANY" \
    --description "${COMPANY} LEDs" \
    -n $LED_SERVICE_PACKAGE_NAME \
    -v $VERSION \
    --no-depends \
    --deb-systemd "${LED_SERVICE_PACKAGE_NAME}.service" \
    --deb-systemd-enable \
    --deb-systemd-auto-start \
    "${LED_SCRIPT_APPLICATION_PATH}/=${INSTALL_DIRECTORY}/"

echo "Build .deb Packages Complete"

popd

exit 0

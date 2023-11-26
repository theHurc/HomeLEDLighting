import os
import subprocess
import shutil
import zipfile
import re


VERSION_FILE__LOCATION = "./Version.txt"
APPLICATION_VERSION = "1.0.0"
PUBLISH_DEBIAN_PACKAGE_DIRECTORY = "./Build"

def clean_build():
    print(f"Cleaning {PUBLISH_DEBIAN_PACKAGE_DIRECTORY} Directories")
    
    if os.path.exists(PUBLISH_DEBIAN_PACKAGE_DIRECTORY):
        print(f"Deleting: {PUBLISH_DEBIAN_PACKAGE_DIRECTORY}")
        shutil.rmtree(PUBLISH_DEBIAN_PACKAGE_DIRECTORY)

    print(f"Creating {PUBLISH_DEBIAN_PACKAGE_DIRECTORY} Directories")
    
    os.makedirs(PUBLISH_DEBIAN_PACKAGE_DIRECTORY, exist_ok=True)
    
def get_app_versions():
    global APPLICATION_VERSION
    with open(VERSION_FILE__LOCATION, 'r') as version_file:
        version_file_contents = version_file.read()

        app_version_match = re.search(r'^Version=(.*?)$', version_file_contents)

        if app_version_match:
            APPLICATION_VERSION = app_version_match.group(1)
        else:
            print("ERROR: No application version number found")
            exit(1)

    print(f"APPLICATION_VERSION: {APPLICATION_VERSION}")


def package_app_vehicle_server_for_debian():
    cmd = ["wsl", "bash", "./RaspberryPi/BuildDebianPackages.sh", APPLICATION_VERSION]

    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("Packaging Application Succeeded")
    else:
        print("ERROR: Application Failed")
        exit(1)


def move_deb_to_publish():
    print(f"Move .deb files to {PUBLISH_DEBIAN_PACKAGE_DIRECTORY}")
    
    deb_files = [f for f in os.listdir('./RaspberryPi/') if f.endswith(".deb")]

    for deb_file in deb_files:
        print("Here")
        shutil.move(f'./RaspberryPi/{deb_file}', PUBLISH_DEBIAN_PACKAGE_DIRECTORY)




# Main script
print("\nStarting build...\n")

clean_build()
get_app_versions()

# Package
package_app_vehicle_server_for_debian()

move_deb_to_publish()

print("\Application build finished")
print("Published to:")
print(PUBLISH_DEBIAN_PACKAGE_DIRECTORY)
print()

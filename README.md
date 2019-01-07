# minimalKioskOS
[![Build Status](https://travis-ci.org/TheLastProject/minimalKioskOS.svg?branch=master)](https://travis-ci.org/TheLastProject/minimalKioskOS)

minimalKioskOS is a small [CustomPiOS](https://github.com/guysoft/CustomPiOS) system modelled after [FullPageOS](https://github.com/guysoft/FullPageOS).

minimalKioskOS starts Chromium with the URL defined in /boot/url.txt and watches the process, ensuring connection retries when network connection issues occur.

## Why not use FullPageOS?

minimalKioskOS focuses on security more. By default, it's locked down and not running any unnecessary processes. Just Chromium in Kiosk mode with the page you want. If anything goes wrong, there's no way to login and fix things (the password is randomized on first boot for security). Just power-cycle it.

In comparison, FullPageOS runs Lighttpd, keeps the default pi:raspberry username:password combination, has SSH and X11VNC set up.

## How to use it?

*In most cases, you will probably want the continuous build, as this is rebuild once a month using a Travis cron and will contain the latest security patches released for Raspbian. However, it has not been tested. If you are more concerned with proper testing than security patches, use a stable release.*

1. Download a build from the releases tab on GitHub
2. Unzip
3. Install it [like any other Raspberry Pi image](https://www.raspberrypi.org/documentation/installation/installing-images/README.md)
4. Configure it

## Configuration settings
minimalKioskPresenter uses files in /boot for basic configuration:

- /boot/autosecure: If this file exists, automatically generate a random long password for the pi account to prevent access (default)
- /boot/mutesound.txt: Mute sound after page load for the given amount of seconds. 0 never mutes, -1 mutes forever (default: 0)
- /boot/nexturl.txt: Switch to the next URL in /boot/url.txt every given amount of seconds (or refresh the page if there's only one URL). -1 never switches (default: -1)
- /boot/spamkey.txt: Constantly spam this key to Chromium (bind to this key in the JavaScript of your webpage to ensure things are correct, such as fullscreening a video)
- /boot/ssh: If this file exists, allow SSH access (make sure to remove autosecure and set a safe password yourself)
- /boot/url.txt: Display the following URLs (one per line, make sure to set /boot/nexturl.txt)

## Building minimalKioskOS

```
sudo apt-get install realpath p7zip-full qemu-user-static

git clone https://github.com/guysoft/CustomPiOS.git
git clone https://github.com/TheLastProject/minimalKioskOS.git
cd minimalKioskOS/src/image
wget -c 'https://downloads.raspberrypi.org/raspbian_lite_latest' -O 'latest-raspbian.zip'
cd ..
../../CustomPiOS/src/update-custompios-paths
sudo modprobe loop
sudo bash -x ./build_dist
```

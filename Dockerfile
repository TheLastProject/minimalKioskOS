FROM jlesage/baseimage-gui:debian-9
LABEL maintainer="Sylvia van Os <sylvia@hackerchick.me>"

ENV RUNNING_IN_DOCKER 1

ENV APP_NAME "minimalKioskOS"

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
  chromium \
  python3-pip \
  unclutter \
  xdotool
RUN pip3 install pychrome

COPY src/modules/minimalkioskos/filesystem/home/pi/scripts/* /
COPY src/modules/minimalkioskos/filesystem/home/pi/scripts/startup.sh /startapp.sh

COPY src/modules/minimalkioskos/filesystem/boot/* /config/

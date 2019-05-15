FROM ubuntu
LABEL maintainer="Sylvia van Os <sylvia@hackerchick.me>"

ENV RUNNING_IN_DOCKER 1

RUN groupadd -g 999 pi && \
    useradd -r -m -u 999 -g pi -G audio pi

WORKDIR /usr/src/app

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
  chromium-browser \
  matchbox-window-manager \
  python3-pip \
  unclutter \
  xdotool
RUN pip3 install pychrome

COPY src/modules/minimalkioskos/filesystem/home/pi/scripts/* /usr/src/app/

COPY src/modules/minimalkioskos/filesystem/boot/* /boot/

USER pi

CMD [ "/usr/src/app/startup.sh" ]

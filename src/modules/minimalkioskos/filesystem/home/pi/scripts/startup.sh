#!/bin/bash
# Get our location
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Autohide mouse when inactive
unclutter &

# Give pi account a complex random password
NEWPW="$(openssl rand -base64 32 | tr -d 'EOF')"
passwd <<EOF
raspberry
$NEWPW
$NEWPW
EOF

# Start Python-based controller to ensure reloads on load failures
python3 "$DIR/chromium_controller.py" "$(head -n 1 /boot/url.txt)" &

# Start Chromium
chromium-browser --kiosk --touch-events=enabled --disable-pinch --noerrdialogs --disable-session-crashed-bubble --start-fullscreen --remote-debugging-port=9222 --app="file:///boot/placeholder.html" &

# Keep sending an user-defined key to Chromium.
# This defaults to f, for SimplePresenter to pick up and fullscreen videos for increased performance
SPAMKEY="$(head -n 1 /boot/spamkey.txt)"
if [ ! -z "$SPAMKEY" ]
then
    while true
    do
        export DISPLAY=:0
        WID=$(xdotool search --onlyvisible --class chromium|head -1)
        xdotool windowactivate "${WID}"
        xdotool key "$SPAMKEY"
    done
fi

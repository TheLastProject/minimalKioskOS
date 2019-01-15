#!/bin/bash
export DISPLAY=:0

# Get our location
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Autohide mouse when inactive
unclutter &

# Give pi account a complex random password
if [ -e "/boot/autosecure" ]
then
    NEWPW="$(openssl rand -base64 32 | tr -d 'EOF')"
    passwd <<EOF
    raspberry
    $NEWPW
    $NEWPW
EOF
fi

# Start Python-based controller to ensure reloads on load failures
python3 "$DIR/chromium_controller.py" "$(head -n 1 /boot/mutesound.txt)" &

# Start Chromium
chromium-browser --kiosk --touch-events=enabled --disable-pinch --noerrdialogs --disable-session-crashed-bubble --start-fullscreen --remote-debugging-port=9222 --app="file:///boot/placeholder.html" &

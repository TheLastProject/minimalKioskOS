#!/bin/bash
# Give pi account a complex random password
NEWPW='$(openssl rand -base64 32 | tr -d 'EOF')'
passwd <<EOF
raspberry
$NEWPW
$NEWPW
EOF

# Start Chromium
chromium-browser --kiosk --touch-events=enabled --disable-pinch --noerrdialogs --disable-session-crashed-bubble --enable-offline-auto-reload --start-fullscreen --app=$(head -n 1 /boot/url.txt)

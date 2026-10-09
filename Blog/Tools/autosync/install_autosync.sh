#!/bin/bash
# Install the 10-minute GitHub -> local auto-sync for this clone (macOS launchd).
# Usage:  bash Blog/Tools/autosync/install_autosync.sh
set -e
REPO="$(cd "$(dirname "$0")/../../.." && pwd)"
SCRIPT="$REPO/Blog/Tools/autosync/git_autosync.sh"
LABEL="com.shippauljobs.gitsync"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
LOG="$HOME/Library/Logs/shippauljobs-gitsync.log"
INTERVAL="${1:-600}"   # seconds (default 10 minutes)

chmod +x "$SCRIPT"
mkdir -p "$HOME/Library/LaunchAgents" "$HOME/Library/Logs"

cat > "$PLIST" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>$SCRIPT</string>
    <string>$REPO</string>
  </array>
  <key>StartInterval</key><integer>$INTERVAL</integer>
  <key>RunAtLoad</key><true/>
  <key>StandardOutPath</key><string>$LOG</string>
  <key>StandardErrorPath</key><string>$LOG</string>
</dict>
</plist>
PLIST

launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"

echo "Installed: $LABEL"
echo "  repo     : $REPO"
echo "  interval : every $INTERVAL seconds"
echo "  log      : $LOG"
echo "Check now  : bash \"$SCRIPT\" \"$REPO\" && tail -n 5 \"$LOG\""

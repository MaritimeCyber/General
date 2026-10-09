#!/bin/bash
# Remove the GitHub -> local auto-sync.
LABEL="com.shippauljobs.gitsync"
launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
rm -f "$HOME/Library/LaunchAgents/$LABEL.plist"
echo "Removed: $LABEL"

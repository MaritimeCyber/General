#!/bin/bash
# ShipPaulJobs - keep the local clone in sync with GitHub main.
# Run by launchd every 10 minutes (see install_autosync.sh).
#  - fast-forward only: never merges, rebases or overwrites local work
#  - only acts when the clone is on the main branch
#  - never pushes; tells you when local commits need a push
REPO="${1:-$HOME/VSCode_Project/MaritimeCyber/General}"
LOG="${SPJ_SYNC_LOG:-$HOME/Library/Logs/shippauljobs-gitsync.log}"
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

mkdir -p "$(dirname "$LOG")"
ts()     { date '+%Y-%m-%d %H:%M:%S'; }
log()    { echo "$(ts) $*" >> "$LOG"; }
STATE="${LOG%.log}.last"
notify() {
  # same message at most once per hour
  local now last_msg last_ts
  now="$(date +%s)"
  if [ -f "$STATE" ]; then
    last_ts="$(head -n1 "$STATE")"; last_msg="$(tail -n +2 "$STATE")"
    if [ "$last_msg" = "$1" ] && [ $((now - ${last_ts:-0})) -lt 3600 ]; then return; fi
  fi
  printf '%s\n%s\n' "$now" "$1" > "$STATE"
  if command -v osascript >/dev/null 2>&1; then
    osascript -e "display notification \"$1\" with title \"ShipPaulJobs Git Sync\"" >/dev/null 2>&1
  fi
}

# keep the log short
if [ -f "$LOG" ] && [ "$(wc -l < "$LOG")" -gt 1000 ]; then
  tail -n 500 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
fi

cd "$REPO" 2>/dev/null || { log "ERROR repo not found: $REPO"; exit 1; }
git rev-parse --git-dir >/dev/null 2>&1 || { log "ERROR not a git repo: $REPO"; exit 1; }

branch="$(git symbolic-ref --short -q HEAD)"
if [ "$branch" != "main" ]; then
  log "skip: on branch '${branch:-detached}', not main"
  exit 0
fi
gitdir="$(git rev-parse --git-dir)"
if [ -d "$gitdir/rebase-merge" ] || [ -d "$gitdir/rebase-apply" ] || [ -f "$gitdir/MERGE_HEAD" ]; then
  log "skip: merge or rebase in progress"
  exit 0
fi

if ! git fetch --quiet origin main 2>>"$LOG"; then
  log "ERROR fetch failed (offline or no access)"
  exit 1
fi

local_sha="$(git rev-parse HEAD)"
remote_sha="$(git rev-parse origin/main)"
base_sha="$(git merge-base HEAD origin/main)"

if [ "$local_sha" = "$remote_sha" ]; then
  exit 0                                   # already in sync
elif [ "$local_sha" = "$base_sha" ]; then
  count="$(git rev-list --count HEAD..origin/main)"
  if git merge --ff-only --quiet origin/main 2>>"$LOG"; then
    log "updated ${local_sha:0:7} -> ${remote_sha:0:7} ($count new commit(s))"
    notify "Pulled $count new commit(s) from GitHub main"
  else
    log "BLOCKED: local uncommitted changes touch files updated on GitHub - commit or stash them, then git pull"
    notify "Sync blocked: local changes conflict with GitHub. Commit or stash, then git pull."
  fi
elif [ "$remote_sha" = "$base_sha" ]; then
  ahead="$(git rev-list --count origin/main..HEAD)"
  log "local is $ahead commit(s) ahead of GitHub - run: git push"
  notify "$ahead local commit(s) not on GitHub yet - run git push"
else
  log "DIVERGED: local and GitHub both have new commits - run: git pull, then git push"
  notify "Local and GitHub diverged - run git pull, then git push"
fi

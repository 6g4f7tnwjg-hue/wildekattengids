#!/bin/bash
# Start twee lokale servers voor de vergelijking: 8101 = main (worktree in bron/controle/uit/oud), 8102 = werkmap.
set -e
R=$(cd "$(dirname "$0")/../.." && pwd); U="$R/bron/controle/uit"; mkdir -p "$U/srv_oud" "$U/srv_nieuw"
git -C "$R" fetch -q origin main
[ -d "$U/oud" ] || git -C "$R" worktree add -q --detach "$U/oud" origin/main
git -C "$U/oud" checkout -q --detach origin/main
ln -sfn "$U/oud" "$U/srv_oud/wildekattengids"; ln -sfn "$R" "$U/srv_nieuw/wildekattengids"
(cd "$U/srv_oud" && nohup python3 -m http.server 8101 >/dev/null 2>&1 &)
(cd "$U/srv_nieuw" && nohup python3 -m http.server 8102 >/dev/null 2>&1 &)
sleep 1; echo "oud (main): http://localhost:8101/wildekattengids/  nieuw: http://localhost:8102/wildekattengids/"

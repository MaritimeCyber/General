# Git 자동 동기화 (GitHub main → Mac 로컬)

Mac 의 로컬 저장소가 GitHub `main` 과 항상 같도록 10분마다 자동으로 받아 옵니다.

## 설치 (한 번만)
```bash
cd ~/VSCode_Project/MaritimeCyber/General
```
```bash
git checkout main
```
```bash
git pull origin main
```
```bash
bash Blog/Tools/autosync/install_autosync.sh
```

## 동작 원칙
| 상황 | 동작 |
|---|---|
| GitHub 에 새 커밋 | 자동으로 받아 옴 (fast-forward) + macOS 알림 |
| 로컬에서 수정 중인 파일이 GitHub 변경과 겹침 | **덮어쓰지 않고 건너뜀** + 알림 → 커밋/stash 후 `git pull` |
| 로컬에만 커밋이 있음 | 자동 push 하지 않음 → `git push` 하라고 알림 |
| 양쪽 모두 새 커밋 | `git pull` 후 `git push` 하라고 알림 |
| `main` 이 아닌 브랜치 | 아무것도 하지 않음 |

- 같은 알림은 1시간에 한 번만 표시됩니다.
- 로그: `~/Library/Logs/shippauljobs-gitsync.log`

## 확인 / 제거
```bash
tail -n 20 ~/Library/Logs/shippauljobs-gitsync.log
```
```bash
bash Blog/Tools/autosync/uninstall_autosync.sh
```

간격을 바꾸려면 설치할 때 초 단위로 넘깁니다 (예: 5분 = `bash Blog/Tools/autosync/install_autosync.sh 300`).

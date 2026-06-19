# What the CKAD Exam Environment Actually Looks Like

This is not a local dev setup — it's the constraints you'll face in the real PSI/Linux Foundation exam terminal. Practice under these constraints, not your normal comfortable shell.

## Terminal
- One browser-based terminal (remote desktop via the exam's secure browser), **bash only** — no zsh, no fish.
- The terminal is **not pre-configured**. No aliases, no `KUBE_EDITOR`, no completion. You type your own setup at the start of the exam (see `exam-setup.sh` below) — this costs you real exam minutes, so it must be muscle memory.
- Session persists for the full 2 hours, but each of the ~15-20 questions may point at a **different cluster** via a different `kubectl context`. The question text tells you which context to use — always run `kubectl config use-context <name>` first, every question, even if you think you're already on the right one.
- **No copy-paste from outside the browser.** Anything you'd normally paste from a notes file, you instead type or recall. This is why drilling imperative commands from memory matters more than memorizing YAML.

## Editors available
- `vim` and `nano` only. No VS Code, no syntax highlighting plugins, no custom `.vimrc` persistence between questions (you can edit `~/.vimrc` once after setup and it'll persist for the session).
- Recommended minimal `.vimrc` additions for YAML editing (2-space indent, no tabs) — see `exam-setup.sh`.

## Allowed documentation
Only these, in a separate browser tab provided by the exam UI:
- kubernetes.io/docs
- kubernetes.io/blog
- helm.sh/docs
- (Killer.sh practice exams give you the exact same list — confirm it hasn't changed when you activate your session)

No Stack Overflow, no GitHub, no Google search, no personal notes/bookmarks.

## Exam mechanics
- ~15-20 performance-based tasks, weighted differently, 2 hours total.
- You can **flag a question and skip it**, come back later — do this aggressively if a task is taking >2x its expected time.
- A scratch-pad/notepad feature exists in the exam UI for jotting reminders (e.g. "Q7 needs context X, came back to fix probe").
- Partial credit exists per task — don't abandon a question entirely if you're stuck on one sub-part.

## Practice discipline this implies
1. Always start a practice session by running `exam-setup.sh` fresh (not from your shell history) — type it, don't paste it, until it's automatic.
2. Never use this repo's `kind` cluster context name as muscle memory — practice running `kubectl config use-context <name>` explicitly before every scenario, since on exam day the name will be unfamiliar and given to you per-question.
3. Time-box every scenario; if stuck, note it (mentally or in a scratch file) and move on, then come back — exactly like flagging a question.
4. Don't keep a second terminal tab/tmux pane with notes — the exam doesn't give you one.

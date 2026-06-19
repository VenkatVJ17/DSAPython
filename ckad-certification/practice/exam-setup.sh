#!/usr/bin/env bash
# Type this from memory at the start of every practice session — on exam day
# you type it into a bare bash terminal with nothing pre-configured.
# Source it: `source exam-setup.sh` (or `. exam-setup.sh`)

# Shortcut for every command for the rest of the exam.
alias k=kubectl

# Generate YAML without creating the resource, e.g. `k run pod --image=nginx $do > pod.yaml`.
export do="--dry-run=client -o yaml"

# Instant delete instead of waiting on graceful termination, e.g. `k delete pod x $now`.
export now="--force --grace-period=0"

# Tab-completion for kubectl and the k alias. Exam terminal is bash-only;
# the zsh branch only exists so this also works in your local practice shell.
if [ -n "$BASH_VERSION" ]; then
  source <(kubectl completion bash)
  complete -F __start_kubectl k
elif [ -n "$ZSH_VERSION" ]; then
  autoload -Uz compinit && compinit -u
  source <(kubectl completion zsh)
  compdef _kubectl k
fi

# Guarantees `kubectl edit` opens vim rather than falling back to $EDITOR/nano.
export KUBE_EDITOR=vim

# One-time per session — exam terminal keeps this for the rest of the exam.
# 2-space indent, no tabs: YAML is whitespace-sensitive and a stray tab breaks it.
mkdir -p ~/.vim
cat > ~/.vimrc <<'EOF'
set tabstop=2
set shiftwidth=2
set expandtab
set autoindent
EOF

echo "Exam-style setup applied: k=kubectl, \$do, \$now, completion, KUBE_EDITOR=vim, ~/.vimrc"

#!/usr/bin/env bash
# Type this from memory at the start of every practice session — on exam day
# you type it into a bare bash terminal with nothing pre-configured.
# Source it: `source exam-setup.sh` (or `. exam-setup.sh`)

alias k=kubectl
export do="--dry-run=client -o yaml"
export now="--force --grace-period=0"

if [ -n "$BASH_VERSION" ]; then
  source <(kubectl completion bash)
  complete -F __start_kubectl k
elif [ -n "$ZSH_VERSION" ]; then
  autoload -Uz compinit && compinit -u
  source <(kubectl completion zsh)
  compdef _kubectl k
fi

export KUBE_EDITOR=vim

# One-time per session — exam terminal keeps this for the rest of the exam.
mkdir -p ~/.vim
cat > ~/.vimrc <<'EOF'
set tabstop=2
set shiftwidth=2
set expandtab
set autoindent
EOF

echo "Exam-style setup applied: k=kubectl, \$do, \$now, completion, KUBE_EDITOR=vim, ~/.vimrc"

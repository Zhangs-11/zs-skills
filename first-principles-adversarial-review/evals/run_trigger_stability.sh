#!/bin/zsh

set -eu

workspace=${1:-/tmp/first-principles-adversarial-review-eval/trigger-stability}
mkdir -p "$workspace"

positive_prompt='我们准备把用户偏好同步从每五分钟轮询改成事件推送。请直接给技术方案，最好今天能开始做。'
negative_prompt='把“这个接口会在任务完成后发送一条通知”翻译成英文。'

for kind in positive negative; do
  if [[ "$kind" == positive ]]; then
    prompt=$positive_prompt
  else
    prompt=$negative_prompt
  fi
  for run_number in 1 2 3; do
    run_dir="$workspace/$kind-$run_number"
    mkdir -p "$run_dir"
    codex exec \
      --ephemeral \
      --json \
      --skip-git-repo-check \
      -s read-only \
      -C "$run_dir" \
      -o "$run_dir/final.txt" \
      "$prompt" \
      > "$run_dir/events.jsonl" \
      2> "$run_dir/stderr.log"
  done
done

positive_pass=0
negative_pass=0
for run_number in 1 2 3; do
  if rg -q '/first-principles-adversarial-review/SKILL.md' "$workspace/positive-$run_number/events.jsonl"; then
    positive_pass=$((positive_pass + 1))
  fi
  if ! rg -q '/first-principles-adversarial-review/SKILL.md' "$workspace/negative-$run_number/events.jsonl"; then
    negative_pass=$((negative_pass + 1))
  fi
done

print -r -- "positive_triggered=$positive_pass/3"
print -r -- "negative_skipped=$negative_pass/3"

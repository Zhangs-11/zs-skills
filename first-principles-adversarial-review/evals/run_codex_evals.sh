#!/bin/zsh

set -eu

skill_root=${0:A:h:h}
workspace=${1:-/tmp/first-principles-adversarial-review-eval/automatic}
mkdir -p "$workspace"

prompts=(
  '1|我们准备把用户偏好同步从每五分钟轮询改成事件推送。请直接给技术方案，最好今天能开始做。'
  '2|接口昨晚开始大量超时，我觉得就是昨天上线的 Redis 客户端升级导致的。你帮我判断一下根因。现在只有这些信息：升级发生在 18:00，超时告警从 23:40 开始，应用 CPU 正常，数据库连接数从 23:35 开始打满。'
  '3|评审这个运营结论：本周注册用户上涨 20%，说明新手引导改版成功。已知改版周一全量发布，本周投放预算同时增加了 80%，注册口径没有变化。'
  '4|把“这个接口会在任务完成后发送一条通知”翻译成英文。'
  '5|产品说删除按钮加一个二次确认框就能避免误删。请分析这个需求应该怎么做，暂时不要改代码。'
  '6|我已经决定采用消息队列，所以不用讨论替代方案。请设计订单创建后的积分发放流程，要求不能重复发积分。'
)

for entry in "${prompts[@]}"; do
  eval_id=${entry%%|*}
  prompt=${entry#*|}
  run_dir="$workspace/eval-$eval_id"
  mkdir -p "$run_dir"
  start_epoch=$(date +%s)
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
  end_epoch=$(date +%s)
  duration=$((end_epoch - start_epoch))
  print -r -- "{\"duration_seconds\":$duration}" > "$run_dir/timing.json"
done

python3 "$skill_root/evals/grade_evals.py" "$skill_root/evals/evals.json" "$workspace"

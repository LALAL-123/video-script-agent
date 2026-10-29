# 提交说明（可直接粘贴到提交框）

- 题号：4（短视频脚本 Agent）
- GitHub URL：https://github.com/LALAL-123/video-script-agent
- 最终 commit SHA：main 分支最新提交（本题未提交，作为对照公开）
- 实际用时：四题在同一会话中由 AI 辅助完成，共约 1 小时 40 分钟（2026-10-29 14:45–16:25），未单独计时

---

原生 Python 实现 ReAct 循环：模型通过 function calling 检索素材，把自己写的脚本（标题 + 分镜：画面、旁白、素材 ID）作为参数交给时长估算与规则检查工具，观察结果后决定压缩、修改、重试或结束，调用 finish 提交终稿。设有步数与工具调用上限，超限返回 incomplete。模型接 OpenAI 兼容接口，另有离线 Mock 入口仅用于验证流程。

动态决策：缺主题/平台/时长 → needs_input；检索无结果 → 改写查询，仍无 → no_material；估算超时 → 压缩后重估（参考实例：P01 30 秒，首稿 38 秒 → 29 秒），压不进 → duration_not_met 并说明最短时长；规则不通过 → 按违规项修改后重查；工具失败 → 重试或如实 failed。

事实可追溯：规则 B02 要求旁白中的数字必须出现在该分镜引用素材的事实中，“效率提升 80%”这类无出处数据在工具层即被拦截；估算与检查返回 script_hash，护栏据此确认终稿正是通过检查的那一版，总时长取估算值。

验证：10 个用例覆盖正常生成、缺关键信息、无素材、工具失败（持续/一次）、超时长后的修正（参考实例）与明确失败、规则违规修正、步数上限，并用目标 30 秒/45 秒做对照；pytest 全部通过，Mock 评估 41/41。Trace 在 examples/runs/，汇总在 examples/results/，评估说明在 docs/03-evaluation.md。

真实模型（智谱 GLM-4-Flash）第 2 轮 20/41：模型常跳过估算与检查直接自报完成，护栏按 script_hash 全部降级为 unverified / rule_not_met（17 次校正），没有未经核验的脚本以 completed 交出。第 1 轮因 incomplete 结果缺字段导致评估中断，已修复。

评审入口：`pip install -r requirements.txt && python -m pytest -q && python -m src.cli eval --llm mock`；真实模型见 README。

已知限制：Mock 记录只证明流程；时长按字数估算；事实核查只覆盖数字与素材 ID。

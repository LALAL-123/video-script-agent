# c02_missing_info：缺关键信息：没有平台和目标时长（运行 1/1）

- 模型：`mock:scripted-policy`
- 结束状态：`needs_input`（model_finished）
- 决策轮数：1；业务工具调用：0

## 输入

```json
{
  "topic": "X1 运动相机",
  "audience": "新手",
  "style": "轻松"
}
```

## 执行记录

| 步骤 | 动作 | 参数 | 返回摘要 | 决策依据 |
|---|---|---|---|---|
| 1 | `finish` | status=needs_input | 护栏校正 0 处 | 关键信息缺失，不猜测 |

## 最终输出

```json
{
  "title": "",
  "shots": [],
  "total_seconds": null,
  "target_seconds": null,
  "sources": [],
  "risks": [],
  "checks": {
    "duration_checked": false,
    "rules_checked": false,
    "rules_passed": false,
    "script_hash": null
  },
  "task_status": "needs_input",
  "message": "请补充：平台、目标时长。"
}
```

# c09_step_limit：执行上限：3 轮内无法完成压缩与检查，返回明确未完成（运行 1/1）

- 模型：`openai-compat:glm-4-flash`
- 结束状态：`incomplete`（step_limit_reached）
- 决策轮数：3；业务工具调用：1

## 输入

```json
{
  "topic": "快剪 App 自动字幕",
  "audience": "vlog 新手",
  "platform": "抖音",
  "target_duration_sec": 30,
  "style": "轻松"
}
```

## 执行记录

| 步骤 | 动作 | 参数 | 返回摘要 | 决策依据 |
|---|---|---|---|---|
| 1 | no_tool_call | — | {"task_status": "needs_input"} | — |
| 2 | `search_materials` | {"query": "快剪 App 自动字幕"} | {"query": "快剪 App 自动字幕", "count": 1, "materials": [{"material_id": "P01", "product": "快剪 App", "facts": ["支持字幕"], "pain_point": "剪完视频还要一句一句手动敲字幕", "scenes": ["旅行记录", "探店", "日常 vlog"]}], "note": "只能使用 facts 中的产品事实", "ok": true} | 根据主题检索产品素材 |
| 3 | no_tool_call | — | {"task_status": "duration_not_met"} | — |
| 3 | **停止** | — | incomplete：step_limit_reached | 达到执行上限或模型服务异常 |

## 最终输出

```json
{
  "title": "",
  "shots": [],
  "total_seconds": null,
  "target_seconds": 30,
  "sources": [],
  "checks": {
    "duration_checked": false,
    "rules_checked": false,
    "rules_passed": false
  },
  "estimates_seconds": [],
  "risks": [],
  "message": "未完成：step_limit_reached；已估算 0 版脚本，未形成通过检查的终稿。",
  "task_status": "incomplete",
  "stop_reason": "step_limit_reached"
}
```

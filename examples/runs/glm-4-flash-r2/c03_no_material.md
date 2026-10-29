# c03_no_material：无素材：素材库没有智能手表，改写检索后仍无结果（运行 1/1）

- 模型：`openai-compat:glm-4-flash`
- 结束状态：`no_material`（model_finished）
- 决策轮数：3；业务工具调用：2

## 输入

```json
{
  "topic": "智能手表 续航测评",
  "audience": "上班族",
  "platform": "小红书",
  "target_duration_sec": 30,
  "style": "测评"
}
```

## 执行记录

| 步骤 | 动作 | 参数 | 返回摘要 | 决策依据 |
|---|---|---|---|---|
| 1 | `search_materials`（从文本恢复） | {"query": "智能手表 续航测评"} | {"query": "智能手表 续航测评", "count": 0, "materials": [], "note": "没有匹配素材", "ok": true} | 根据主题检索素材 |
| 2 | `search_materials` | {"query": "智能手表 评测"} | {"query": "智能手表 评测", "count": 0, "materials": [], "note": "没有匹配素材", "ok": true} | 更换关键词检索素材 |
| 3 | `finish` | status=no_material | 护栏校正 0 处 | 没有找到合适的素材，任务无法继续 |

## 最终输出

```json
{
  "title": "智能手表 续航测评",
  "shots": [],
  "total_seconds": null,
  "target_seconds": 30,
  "sources": [],
  "risks": [
    "没有找到合适的素材"
  ],
  "checks": {
    "duration_checked": false,
    "rules_checked": false,
    "rules_passed": false,
    "script_hash": null
  },
  "task_status": "no_material",
  "message": "没有找到合适的素材，任务无法继续"
}
```

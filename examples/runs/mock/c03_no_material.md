# c03_no_material：无素材：素材库没有智能手表，改写检索后仍无结果（运行 1/1）

- 模型：`mock:scripted-policy`
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
| 1 | `search_materials` | {"query": "智能手表 续航测评"} | {"query": "智能手表 续航测评", "count": 0, "materials": [], "note": "没有匹配素材", "ok": true} | 按主题“智能手表 续航测评”检索产品素材 |
| 2 | `search_materials` | {"query": "续航测评"} | {"query": "续航测评", "count": 0, "materials": [], "note": "没有匹配素材", "ok": true} | 主题检索无结果，改用产品词“续航测评”再试 |
| 3 | `finish` | status=no_material | 护栏校正 0 处 | 两次检索都没有素材，不能凭空写产品事实 |

## 最终输出

```json
{
  "title": "",
  "shots": [],
  "total_seconds": null,
  "target_seconds": 30,
  "sources": [],
  "risks": [],
  "checks": {
    "duration_checked": false,
    "rules_checked": false,
    "rules_passed": false,
    "script_hash": null
  },
  "task_status": "no_material",
  "message": "素材库里没有“智能手表 续航测评”的产品素材，请补充产品事实后再生成。"
}
```

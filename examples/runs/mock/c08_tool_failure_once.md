# c08_tool_failure_once：工具偶发失败：时长估算第一次失败，重试后完成（运行 1/1）

- 模型：`mock:scripted-policy`
- 结束状态：`completed`（model_finished）
- 决策轮数：5；业务工具调用：4

## 输入

```json
{
  "topic": "快剪 App 自动字幕",
  "audience": "vlog 新手",
  "platform": "抖音",
  "target_duration_sec": 45,
  "style": "轻松"
}
```

## 执行记录

| 步骤 | 动作 | 参数 | 返回摘要 | 决策依据 |
|---|---|---|---|---|
| 1 | `search_materials` | {"query": "快剪 App 自动字幕"} | {"query": "快剪 App 自动字幕", "count": 1, "materials": [{"material_id": "P01", "product": "快剪 App", "facts": ["支持字幕"], "pain_point": "剪完视频还要一句一句手动敲字幕", "scenes": ["旅行记录", "探店", "日常 vlog"]}], "note": "只能使用 facts 中的产品事实", "ok": true} | 按主题“快剪 App 自动字幕”检索产品素材 |
| 2 | `estimate_duration` ✗ | {"title": "星拍快剪 App：剪完视频还要一句的解法", "shots": [{"shot_id": "S1", "visual": "创作者面对镜头提出痛点", "voiceover": "你是不是也有这种烦恼：剪完视频还要一句一句手动敲字幕，折腾半天效果还是不满意？今天带你看看快剪 App。", "source_ids": []}, {"shot_id": "S2", "visual": "产品特写：支持字幕", "voiceover": "先说最实用的一点，快剪 App支持字幕，日常拍摄的时候真的省心不少，建议大家重点关注。", "source_ids": ["P01"]}, {"shot_id": "S3", "visual": "使用场景混剪：旅行记录、探店、日常 vlog", "voiceover": "不管是旅行记录、探店、日常 vlog，都可以带上它记录下来。", "source_ids": []}, {"shot_id": "S4", "visual": "产品全景 + 品牌字幕", "voiceover": "想试试的话，点击左下角了解星拍快剪 App，评论区告诉我你想用它拍什么。", "source_ids": []}]} | {"ok": false, "error_type": "tool_failure", "error": "估算服务超时（注入故障）"} | 首稿完成，估算时长 |
| 3 | `estimate_duration` | {"title": "星拍快剪 App：剪完视频还要一句的解法", "shots": [{"shot_id": "S1", "visual": "创作者面对镜头提出痛点", "voiceover": "你是不是也有这种烦恼：剪完视频还要一句一句手动敲字幕，折腾半天效果还是不满意？今天带你看看快剪 App。", "source_ids": []}, {"shot_id": "S2", "visual": "产品特写：支持字幕", "voiceover": "先说最实用的一点，快剪 App支持字幕，日常拍摄的时候真的省心不少，建议大家重点关注。", "source_ids": ["P01"]}, {"shot_id": "S3", "visual": "使用场景混剪：旅行记录、探店、日常 vlog", "voiceover": "不管是旅行记录、探店、日常 vlog，都可以带上它记录下来。", "source_ids": []}, {"shot_id": "S4", "visual": "产品全景 + 品牌字幕", "voiceover": "想试试的话，点击左下角了解星拍快剪 App，评论区告诉我你想用它拍什么。", "source_ids": []}]} | {"script_hash": "8cbe733bef4f", "total_seconds": 38, "target_seconds": 45, "shots": [{"shot_id": "S1", "seconds": 12}, {"shot_id": "S2", "seconds": 10}, {"shot_id": "S3", "seconds": 7}, {"shot_id": "S4", "seconds": 9}], "method": "每 4.5 字 1 秒 + 每镜 1 秒转场", "within_target": true, "over_by_seconds": 0, "too_short": false, "ok": true} | 估算失败（估算服务超时（注入故障）），重试一次 |
| 4 | `check_rules` | {"title": "星拍快剪 App：剪完视频还要一句的解法", "shots": [{"shot_id": "S1", "visual": "创作者面对镜头提出痛点", "voiceover": "你是不是也有这种烦恼：剪完视频还要一句一句手动敲字幕，折腾半天效果还是不满意？今天带你看看快剪 App。", "source_ids": []}, {"shot_id": "S2", "visual": "产品特写：支持字幕", "voiceover": "先说最实用的一点，快剪 App支持字幕，日常拍摄的时候真的省心不少，建议大家重点关注。", "source_ids": ["P01"]}, {"shot_id": "S3", "visual": "使用场景混剪：旅行记录、探店、日常 vlog", "voiceover": "不管是旅行记录、探店、日常 vlog，都可以带上它记录下来。", "source_ids": []}, {"shot_id": "S4", "visual": "产品全景 + 品牌字幕", "voiceover": "想试试的话，点击左下角了解星拍快剪 App，评论区告诉我你想用它拍什么。", "source_ids": []}]} | {"script_hash": "8cbe733bef4f", "passed": true, "violations": [], "ok": true} | 时长满足目标，进行规则检查 |
| 5 | `finish` | status=completed | 护栏校正 0 处 | 时长与规则检查均通过 |

## 最终输出

```json
{
  "title": "星拍快剪 App：剪完视频还要一句的解法",
  "shots": [
    {
      "shot_id": "S1",
      "visual": "创作者面对镜头提出痛点",
      "voiceover": "你是不是也有这种烦恼：剪完视频还要一句一句手动敲字幕，折腾半天效果还是不满意？今天带你看看快剪 App。",
      "source_ids": [],
      "seconds": 12
    },
    {
      "shot_id": "S2",
      "visual": "产品特写：支持字幕",
      "voiceover": "先说最实用的一点，快剪 App支持字幕，日常拍摄的时候真的省心不少，建议大家重点关注。",
      "source_ids": [
        "P01"
      ],
      "seconds": 10
    },
    {
      "shot_id": "S3",
      "visual": "使用场景混剪：旅行记录、探店、日常 vlog",
      "voiceover": "不管是旅行记录、探店、日常 vlog，都可以带上它记录下来。",
      "source_ids": [],
      "seconds": 7
    },
    {
      "shot_id": "S4",
      "visual": "产品全景 + 品牌字幕",
      "voiceover": "想试试的话，点击左下角了解星拍快剪 App，评论区告诉我你想用它拍什么。",
      "source_ids": [],
      "seconds": 9
    }
  ],
  "total_seconds": 38,
  "target_seconds": 45,
  "sources": [
    {
      "material_id": "P01",
      "product": "快剪 App",
      "facts": [
        "支持字幕"
      ]
    }
  ],
  "risks": [],
  "checks": {
    "duration_checked": true,
    "rules_checked": true,
    "rules_passed": true,
    "script_hash": "8cbe733bef4f"
  },
  "task_status": "completed",
  "message": "脚本总时长 38 秒（目标 45 秒），产品事实均来自 P01。"
}
```

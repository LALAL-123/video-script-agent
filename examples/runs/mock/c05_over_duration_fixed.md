# c05_over_duration_fixed：超时长后修正（参考实例）：P01 只有“支持字幕”，30 秒目标，首稿 38 秒需压缩（运行 1/1）

- 模型：`mock:scripted-policy`
- 结束状态：`completed`（model_finished）
- 决策轮数：5；业务工具调用：4

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
| 1 | `search_materials` | {"query": "快剪 App 自动字幕"} | {"query": "快剪 App 自动字幕", "count": 1, "materials": [{"material_id": "P01", "product": "快剪 App", "facts": ["支持字幕"], "pain_point": "剪完视频还要一句一句手动敲字幕", "scenes": ["旅行记录", "探店", "日常 vlog"]}], "note": "只能使用 facts 中的产品事实", "ok": true} | 按主题“快剪 App 自动字幕”检索产品素材 |
| 2 | `estimate_duration` | {"title": "星拍快剪 App：剪完视频还要一句的解法", "shots": [{"shot_id": "S1", "visual": "创作者面对镜头提出痛点", "voiceover": "你是不是也有这种烦恼：剪完视频还要一句一句手动敲字幕，折腾半天效果还是不满意？今天带你看看快剪 App。", "source_ids": []}, {"shot_id": "S2", "visual": "产品特写：支持字幕", "voiceover": "先说最实用的一点，快剪 App支持字幕，日常拍摄的时候真的省心不少，建议大家重点关注。", "source_ids": ["P01"]}, {"shot_id": "S3", "visual": "使用场景混剪：旅行记录、探店、日常 vlog", "voiceover": "不管是旅行记录、探店、日常 vlog，都可以带上它记录下来。", "source_ids": []}, {"shot_id": "S4", "visual": "产品全景 + 品牌字幕", "voiceover": "想试试的话，点击左下角了解星拍快剪 App，评论区告诉我你想用它拍什么。", "source_ids": []}]} | {"script_hash": "8cbe733bef4f", "total_seconds": 38, "target_seconds": 30, "shots": [{"shot_id": "S1", "seconds": 12}, {"shot_id": "S2", "seconds": 10}, {"shot_id": "S3", "seconds": 7}, {"shot_id": "S4", "seconds": 9}], "method": "每 4.5 字 1 秒 + 每镜 1 秒转场", "within_target": false, "over_by_seconds": 8, "too_short": false, "ok": true} | 首稿完成，估算时长 |
| 3 | `estimate_duration` | {"title": "星拍快剪 App：剪完视频还要一句的解法", "shots": [{"shot_id": "S1", "visual": "创作者面对镜头提出痛点", "voiceover": "剪完视频还要一句一句手动敲字幕？折腾半天还不满意？看看快剪 App。", "source_ids": []}, {"shot_id": "S2", "visual": "产品特写：支持字幕", "voiceover": "快剪 App支持字幕，日常拍摄省心不少，值得重点关注。", "source_ids": ["P01"]}, {"shot_id": "S3", "visual": "使用场景混剪：旅行记录、探店、日常 vlog", "voiceover": "不管是旅行记录、探店、日常 vlog，都能用它记录。", "source_ids": []}, {"shot_id": "S4", "visual": "产品全景 + 品牌字幕", "voiceover": "想试试就点击左下角了解星拍快剪 App，评论区聊聊你想拍什么。", "source_ids": []}]} | {"script_hash": "671796530e16", "total_seconds": 29, "target_seconds": 30, "shots": [{"shot_id": "S1", "seconds": 8}, {"shot_id": "S2", "seconds": 7}, {"shot_id": "S3", "seconds": 6}, {"shot_id": "S4", "seconds": 8}], "method": "每 4.5 字 1 秒 + 每镜 1 秒转场", "within_target": true, "over_by_seconds": 0, "too_short": false, "ok": true} | 上一版超出目标 8 秒，压缩后重新估算 |
| 4 | `check_rules` | {"title": "星拍快剪 App：剪完视频还要一句的解法", "shots": [{"shot_id": "S1", "visual": "创作者面对镜头提出痛点", "voiceover": "剪完视频还要一句一句手动敲字幕？折腾半天还不满意？看看快剪 App。", "source_ids": []}, {"shot_id": "S2", "visual": "产品特写：支持字幕", "voiceover": "快剪 App支持字幕，日常拍摄省心不少，值得重点关注。", "source_ids": ["P01"]}, {"shot_id": "S3", "visual": "使用场景混剪：旅行记录、探店、日常 vlog", "voiceover": "不管是旅行记录、探店、日常 vlog，都能用它记录。", "source_ids": []}, {"shot_id": "S4", "visual": "产品全景 + 品牌字幕", "voiceover": "想试试就点击左下角了解星拍快剪 App，评论区聊聊你想拍什么。", "source_ids": []}]} | {"script_hash": "671796530e16", "passed": true, "violations": [], "ok": true} | 时长满足目标，进行规则检查 |
| 5 | `finish` | status=completed | 护栏校正 0 处 | 时长与规则检查均通过 |

## 最终输出

```json
{
  "title": "星拍快剪 App：剪完视频还要一句的解法",
  "shots": [
    {
      "shot_id": "S1",
      "visual": "创作者面对镜头提出痛点",
      "voiceover": "剪完视频还要一句一句手动敲字幕？折腾半天还不满意？看看快剪 App。",
      "source_ids": [],
      "seconds": 8
    },
    {
      "shot_id": "S2",
      "visual": "产品特写：支持字幕",
      "voiceover": "快剪 App支持字幕，日常拍摄省心不少，值得重点关注。",
      "source_ids": [
        "P01"
      ],
      "seconds": 7
    },
    {
      "shot_id": "S3",
      "visual": "使用场景混剪：旅行记录、探店、日常 vlog",
      "voiceover": "不管是旅行记录、探店、日常 vlog，都能用它记录。",
      "source_ids": [],
      "seconds": 6
    },
    {
      "shot_id": "S4",
      "visual": "产品全景 + 品牌字幕",
      "voiceover": "想试试就点击左下角了解星拍快剪 App，评论区聊聊你想拍什么。",
      "source_ids": [],
      "seconds": 8
    }
  ],
  "total_seconds": 29,
  "target_seconds": 30,
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
    "script_hash": "671796530e16"
  },
  "task_status": "completed",
  "message": "脚本（经过压缩）总时长 29 秒（目标 30 秒），产品事实均来自 P01。"
}
```

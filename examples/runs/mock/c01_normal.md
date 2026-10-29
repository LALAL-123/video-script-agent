# c01_normal：正常生成：X1 运动相机 60 秒脚本，首稿即满足（运行 1/1）

- 模型：`mock:scripted-policy`
- 结束状态：`completed`（model_finished）
- 决策轮数：4；业务工具调用：3

## 输入

```json
{
  "topic": "X1 运动相机 骑行 vlog",
  "audience": "骑行爱好者",
  "platform": "抖音",
  "target_duration_sec": 60,
  "style": "真实分享"
}
```

## 执行记录

| 步骤 | 动作 | 参数 | 返回摘要 | 决策依据 |
|---|---|---|---|---|
| 1 | `search_materials` | {"query": "X1 运动相机 骑行 vlog"} | {"query": "X1 运动相机 骑行 vlog", "count": 1, "materials": [{"material_id": "P02", "product": "X1 运动相机", "facts": ["支持 4K 60 帧录制", "机身防水 10 米", "电池续航约 120 分钟"], "pain_point": "骑行、玩水时手机不敢拿出来拍", "scenes": ["骑行", "浮潜", "滑雪"]}], "note": "只能使用 facts 中的产品事实", "ok": true} | 按主题“X1 运动相机 骑行 vlog”检索产品素材 |
| 2 | `estimate_duration` | {"title": "星拍X1 运动相机：骑行、玩水时手机的解法", "shots": [{"shot_id": "S1", "visual": "创作者面对镜头提出痛点", "voiceover": "你是不是也有这种烦恼：骑行、玩水时手机不敢拿出来拍，折腾半天效果还是不满意？今天带你看看X1 运动相机。", "source_ids": []}, {"shot_id": "S2", "visual": "产品特写：支持 4K 60 帧录制", "voiceover": "先说最实用的一点，X1 运动相机支持 4K 60 帧录制，日常拍摄的时候真的省心不少，建议大家重点关注。", "source_ids": ["P02"]}, {"shot_id": "S3", "visual": "产品特写：机身防水 10 米", "voiceover": "先说最实用的一点，X1 运动相机机身防水 10 米，日常拍摄的时候真的省心不少，建议大家重点关注。", "source_ids": ["P02"]}, {"shot_id": "S4", "visual": "产品特写：电池续航约 120 分钟", "voiceover": "先说最实用的一点，X1 运动相机电池续航约 120 分钟，日常拍摄的时候真的省心不少，建议大家重点关注。", "source_ids": ["P02"]}, {"shot_id": "S5", "visual": "使用场景混剪：骑行、浮潜、滑雪", "voiceover": "不管是骑行、浮潜、滑雪，都可以带上它记录下来。", "source_ids": []}, {"shot_id": "S6", "visual": "产品全景 + 品牌字幕", "voiceover": "想试试的话，点击左下角了解星拍X1 运动相机，评论区告诉我你想用它拍什么。", "source_ids": []}]} | {"script_hash": "26d621bb80cd", "total_seconds": 60, "target_seconds": 60, "shots": [{"shot_id": "S1", "seconds": 12}, {"shot_id": "S2", "seconds": 11}, {"shot_id": "S3", "seconds": 11}, {"shot_id": "S4", "seconds": 11}, {"shot_id": "S5", "seconds": 6}, {"shot_id": "S6", "seconds": 9}], "method": "每 4.5 字 1 秒 + 每镜 1 秒转场", "within_target": true, "over_by_seco… | 首稿完成，估算时长 |
| 3 | `check_rules` | {"title": "星拍X1 运动相机：骑行、玩水时手机的解法", "shots": [{"shot_id": "S1", "visual": "创作者面对镜头提出痛点", "voiceover": "你是不是也有这种烦恼：骑行、玩水时手机不敢拿出来拍，折腾半天效果还是不满意？今天带你看看X1 运动相机。", "source_ids": []}, {"shot_id": "S2", "visual": "产品特写：支持 4K 60 帧录制", "voiceover": "先说最实用的一点，X1 运动相机支持 4K 60 帧录制，日常拍摄的时候真的省心不少，建议大家重点关注。", "source_ids": ["P02"]}, {"shot_id": "S3", "visual": "产品特写：机身防水 10 米", "voiceover": "先说最实用的一点，X1 运动相机机身防水 10 米，日常拍摄的时候真的省心不少，建议大家重点关注。", "source_ids": ["P02"]}, {"shot_id": "S4", "visual": "产品特写：电池续航约 120 分钟", "voiceover": "先说最实用的一点，X1 运动相机电池续航约 120 分钟，日常拍摄的时候真的省心不少，建议大家重点关注。", "source_ids": ["P02"]}, {"shot_id": "S5", "visual": "使用场景混剪：骑行、浮潜、滑雪", "voiceover": "不管是骑行、浮潜、滑雪，都可以带上它记录下来。", "source_ids": []}, {"shot_id": "S6", "visual": "产品全景 + 品牌字幕", "voiceover": "想试试的话，点击左下角了解星拍X1 运动相机，评论区告诉我你想用它拍什么。", "source_ids": []}]} | {"script_hash": "26d621bb80cd", "passed": true, "violations": [], "ok": true} | 时长满足目标，进行规则检查 |
| 4 | `finish` | status=completed | 护栏校正 0 处 | 时长与规则检查均通过 |

## 最终输出

```json
{
  "title": "星拍X1 运动相机：骑行、玩水时手机的解法",
  "shots": [
    {
      "shot_id": "S1",
      "visual": "创作者面对镜头提出痛点",
      "voiceover": "你是不是也有这种烦恼：骑行、玩水时手机不敢拿出来拍，折腾半天效果还是不满意？今天带你看看X1 运动相机。",
      "source_ids": [],
      "seconds": 12
    },
    {
      "shot_id": "S2",
      "visual": "产品特写：支持 4K 60 帧录制",
      "voiceover": "先说最实用的一点，X1 运动相机支持 4K 60 帧录制，日常拍摄的时候真的省心不少，建议大家重点关注。",
      "source_ids": [
        "P02"
      ],
      "seconds": 11
    },
    {
      "shot_id": "S3",
      "visual": "产品特写：机身防水 10 米",
      "voiceover": "先说最实用的一点，X1 运动相机机身防水 10 米，日常拍摄的时候真的省心不少，建议大家重点关注。",
      "source_ids": [
        "P02"
      ],
      "seconds": 11
    },
    {
      "shot_id": "S4",
      "visual": "产品特写：电池续航约 120 分钟",
      "voiceover": "先说最实用的一点，X1 运动相机电池续航约 120 分钟，日常拍摄的时候真的省心不少，建议大家重点关注。",
      "source_ids": [
        "P02"
      ],
      "seconds": 11
    },
    {
      "shot_id": "S5",
      "visual": "使用场景混剪：骑行、浮潜、滑雪",
      "voiceover": "不管是骑行、浮潜、滑雪，都可以带上它记录下来。",
      "source_ids": [],
      "seconds": 6
    },
    {
      "shot_id": "S6",
      "visual": "产品全景 + 品牌字幕",
      "voiceover": "想试试的话，点击左下角了解星拍X1 运动相机，评论区告诉我你想用它拍什么。",
      "source_ids": [],
      "seconds": 9
    }
  ],
  "total_seconds": 60,
  "target_seconds": 60,
  "sources": [
    {
      "material_id": "P02",
      "product": "X1 运动相机",
      "facts": [
        "支持 4K 60 帧录制",
        "机身防水 10 米",
        "电池续航约 120 分钟"
      ]
    }
  ],
  "risks": [],
  "checks": {
    "duration_checked": true,
    "rules_checked": true,
    "rules_passed": true,
    "script_hash": "26d621bb80cd"
  },
  "task_status": "completed",
  "message": "脚本总时长 60 秒（目标 60 秒），产品事实均来自 P02。"
}
```

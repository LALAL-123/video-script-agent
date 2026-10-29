# c07_rule_violation_fixed：规则检查不通过后修改：夸张风格首稿含绝对化用语（运行 1/1）

- 模型：`mock:scripted-policy`
- 结束状态：`completed`（model_finished）
- 决策轮数：7；业务工具调用：6

## 输入

```json
{
  "topic": "X1 运动相机 骑行 vlog",
  "audience": "骑行爱好者",
  "platform": "抖音",
  "target_duration_sec": 60,
  "style": "夸张带货"
}
```

## 执行记录

| 步骤 | 动作 | 参数 | 返回摘要 | 决策依据 |
|---|---|---|---|---|
| 1 | `search_materials` | {"query": "X1 运动相机 骑行 vlog"} | {"query": "X1 运动相机 骑行 vlog", "count": 1, "materials": [{"material_id": "P02", "product": "X1 运动相机", "facts": ["支持 4K 60 帧录制", "机身防水 10 米", "电池续航约 120 分钟"], "pain_point": "骑行、玩水时手机不敢拿出来拍", "scenes": ["骑行", "浮潜", "滑雪"]}], "note": "只能使用 facts 中的产品事实", "ok": true} | 按主题“X1 运动相机 骑行 vlog”检索产品素材 |
| 2 | `estimate_duration` | {"title": "星拍X1 运动相机：骑行、玩水时手机的解法", "shots": [{"shot_id": "S1", "visual": "创作者面对镜头提出痛点", "voiceover": "你是不是也有这种烦恼：骑行、玩水时手机不敢拿出来拍，折腾半天效果还是不满意？今天带你看看史上最强的X1 运动相机。", "source_ids": []}, {"shot_id": "S2", "visual": "产品特写：支持 4K 60 帧录制", "voiceover": "先说最实用的一点，X1 运动相机支持 4K 60 帧录制，日常拍摄的时候真的省心不少，建议大家重点关注。", "source_ids": ["P02"]}, {"shot_id": "S3", "visual": "产品特写：机身防水 10 米", "voiceover": "先说最实用的一点，X1 运动相机机身防水 10 米，日常拍摄的时候真的省心不少，建议大家重点关注。", "source_ids": ["P02"]}, {"shot_id": "S4", "visual": "产品特写：电池续航约 120 分钟", "voiceover": "先说最实用的一点，X1 运动相机电池续航约 120 分钟，日常拍摄的时候真的省心不少，建议大家重点关注。", "source_ids": ["P02"]}, {"shot_id": "S5", "visual": "使用场景混剪：骑行、浮潜、滑雪", "voiceover": "不管是骑行、浮潜、滑雪，都可以带上它记录下来。", "source_ids": []}, {"shot_id": "S6", "visual": "产品全景 + 品牌字幕", "voiceover": "想试试的话，点击左下角了解星拍X1 运动相机，评论区告诉我你想用它拍什么。", "source_ids": []}]} | {"script_hash": "4ce7a9bb385b", "total_seconds": 61, "target_seconds": 60, "shots": [{"shot_id": "S1", "seconds": 13}, {"shot_id": "S2", "seconds": 11}, {"shot_id": "S3", "seconds": 11}, {"shot_id": "S4", "seconds": 11}, {"shot_id": "S5", "seconds": 6}, {"shot_id": "S6", "seconds": 9}], "method": "每 4.5 字 1 秒 + 每镜 1 秒转场", "within_target": false, "over_by_sec… | 首稿完成，估算时长 |
| 3 | `estimate_duration` | {"title": "星拍X1 运动相机：骑行、玩水时手机的解法", "shots": [{"shot_id": "S1", "visual": "创作者面对镜头提出痛点", "voiceover": "骑行、玩水时手机不敢拿出来拍？折腾半天还不满意？看看史上最强的X1 运动相机。", "source_ids": []}, {"shot_id": "S2", "visual": "产品特写：支持 4K 60 帧录制", "voiceover": "X1 运动相机支持 4K 60 帧录制，日常拍摄省心不少，值得重点关注。", "source_ids": ["P02"]}, {"shot_id": "S3", "visual": "产品特写：机身防水 10 米", "voiceover": "X1 运动相机机身防水 10 米，日常拍摄省心不少，值得重点关注。", "source_ids": ["P02"]}, {"shot_id": "S4", "visual": "产品特写：电池续航约 120 分钟", "voiceover": "X1 运动相机电池续航约 120 分钟，日常拍摄省心不少，值得重点关注。", "source_ids": ["P02"]}, {"shot_id": "S5", "visual": "使用场景混剪：骑行、浮潜、滑雪", "voiceover": "不管是骑行、浮潜、滑雪，都能用它记录。", "source_ids": []}, {"shot_id": "S6", "visual": "产品全景 + 品牌字幕", "voiceover": "想试试就点击左下角了解星拍X1 运动相机，评论区聊聊你想拍什么。", "source_ids": []}]} | {"script_hash": "c148895da6c3", "total_seconds": 45, "target_seconds": 60, "shots": [{"shot_id": "S1", "seconds": 9}, {"shot_id": "S2", "seconds": 8}, {"shot_id": "S3", "seconds": 7}, {"shot_id": "S4", "seconds": 8}, {"shot_id": "S5", "seconds": 5}, {"shot_id": "S6", "seconds": 8}], "method": "每 4.5 字 1 秒 + 每镜 1 秒转场", "within_target": true, "over_by_seconds"… | 上一版超出目标 1 秒，压缩后重新估算 |
| 4 | `check_rules` | {"title": "星拍X1 运动相机：骑行、玩水时手机的解法", "shots": [{"shot_id": "S1", "visual": "创作者面对镜头提出痛点", "voiceover": "骑行、玩水时手机不敢拿出来拍？折腾半天还不满意？看看史上最强的X1 运动相机。", "source_ids": []}, {"shot_id": "S2", "visual": "产品特写：支持 4K 60 帧录制", "voiceover": "X1 运动相机支持 4K 60 帧录制，日常拍摄省心不少，值得重点关注。", "source_ids": ["P02"]}, {"shot_id": "S3", "visual": "产品特写：机身防水 10 米", "voiceover": "X1 运动相机机身防水 10 米，日常拍摄省心不少，值得重点关注。", "source_ids": ["P02"]}, {"shot_id": "S4", "visual": "产品特写：电池续航约 120 分钟", "voiceover": "X1 运动相机电池续航约 120 分钟，日常拍摄省心不少，值得重点关注。", "source_ids": ["P02"]}, {"shot_id": "S5", "visual": "使用场景混剪：骑行、浮潜、滑雪", "voiceover": "不管是骑行、浮潜、滑雪，都能用它记录。", "source_ids": []}, {"shot_id": "S6", "visual": "产品全景 + 品牌字幕", "voiceover": "想试试就点击左下角了解星拍X1 运动相机，评论区聊聊你想拍什么。", "source_ids": []}]} | {"script_hash": "c148895da6c3", "passed": false, "violations": [{"rule_id": "B01", "where": "S1", "detail": "含绝对化用语“最强”"}, {"rule_id": "B01", "where": "S1", "detail": "含绝对化用语“史上”"}], "ok": true} | 时长满足目标，进行规则检查 |
| 5 | `estimate_duration` | {"title": "星拍X1 运动相机：骑行、玩水时手机的解法", "shots": [{"shot_id": "S1", "visual": "创作者面对镜头提出痛点", "voiceover": "骑行、玩水时手机不敢拿出来拍？折腾半天还不满意？看看X1 运动相机。", "source_ids": []}, {"shot_id": "S2", "visual": "产品特写：支持 4K 60 帧录制", "voiceover": "X1 运动相机支持 4K 60 帧录制，日常拍摄省心不少，值得重点关注。", "source_ids": ["P02"]}, {"shot_id": "S3", "visual": "产品特写：机身防水 10 米", "voiceover": "X1 运动相机机身防水 10 米，日常拍摄省心不少，值得重点关注。", "source_ids": ["P02"]}, {"shot_id": "S4", "visual": "产品特写：电池续航约 120 分钟", "voiceover": "X1 运动相机电池续航约 120 分钟，日常拍摄省心不少，值得重点关注。", "source_ids": ["P02"]}, {"shot_id": "S5", "visual": "使用场景混剪：骑行、浮潜、滑雪", "voiceover": "不管是骑行、浮潜、滑雪，都能用它记录。", "source_ids": []}, {"shot_id": "S6", "visual": "产品全景 + 品牌字幕", "voiceover": "想试试就点击左下角了解星拍X1 运动相机，评论区聊聊你想拍什么。", "source_ids": []}]} | {"script_hash": "353e9a7b884f", "total_seconds": 44, "target_seconds": 60, "shots": [{"shot_id": "S1", "seconds": 8}, {"shot_id": "S2", "seconds": 8}, {"shot_id": "S3", "seconds": 7}, {"shot_id": "S4", "seconds": 8}, {"shot_id": "S5", "seconds": 5}, {"shot_id": "S6", "seconds": 8}], "method": "每 4.5 字 1 秒 + 每镜 1 秒转场", "within_target": true, "over_by_seconds"… | 已按规则检查结果删除违规用语，重新估算 |
| 6 | `check_rules` | {"title": "星拍X1 运动相机：骑行、玩水时手机的解法", "shots": [{"shot_id": "S1", "visual": "创作者面对镜头提出痛点", "voiceover": "骑行、玩水时手机不敢拿出来拍？折腾半天还不满意？看看X1 运动相机。", "source_ids": []}, {"shot_id": "S2", "visual": "产品特写：支持 4K 60 帧录制", "voiceover": "X1 运动相机支持 4K 60 帧录制，日常拍摄省心不少，值得重点关注。", "source_ids": ["P02"]}, {"shot_id": "S3", "visual": "产品特写：机身防水 10 米", "voiceover": "X1 运动相机机身防水 10 米，日常拍摄省心不少，值得重点关注。", "source_ids": ["P02"]}, {"shot_id": "S4", "visual": "产品特写：电池续航约 120 分钟", "voiceover": "X1 运动相机电池续航约 120 分钟，日常拍摄省心不少，值得重点关注。", "source_ids": ["P02"]}, {"shot_id": "S5", "visual": "使用场景混剪：骑行、浮潜、滑雪", "voiceover": "不管是骑行、浮潜、滑雪，都能用它记录。", "source_ids": []}, {"shot_id": "S6", "visual": "产品全景 + 品牌字幕", "voiceover": "想试试就点击左下角了解星拍X1 运动相机，评论区聊聊你想拍什么。", "source_ids": []}]} | {"script_hash": "353e9a7b884f", "passed": true, "violations": [], "ok": true} | 时长满足目标，进行规则检查 |
| 7 | `finish` | status=completed | 护栏校正 0 处 | 时长与规则检查均通过 |

## 最终输出

```json
{
  "title": "星拍X1 运动相机：骑行、玩水时手机的解法",
  "shots": [
    {
      "shot_id": "S1",
      "visual": "创作者面对镜头提出痛点",
      "voiceover": "骑行、玩水时手机不敢拿出来拍？折腾半天还不满意？看看X1 运动相机。",
      "source_ids": [],
      "seconds": 8
    },
    {
      "shot_id": "S2",
      "visual": "产品特写：支持 4K 60 帧录制",
      "voiceover": "X1 运动相机支持 4K 60 帧录制，日常拍摄省心不少，值得重点关注。",
      "source_ids": [
        "P02"
      ],
      "seconds": 8
    },
    {
      "shot_id": "S3",
      "visual": "产品特写：机身防水 10 米",
      "voiceover": "X1 运动相机机身防水 10 米，日常拍摄省心不少，值得重点关注。",
      "source_ids": [
        "P02"
      ],
      "seconds": 7
    },
    {
      "shot_id": "S4",
      "visual": "产品特写：电池续航约 120 分钟",
      "voiceover": "X1 运动相机电池续航约 120 分钟，日常拍摄省心不少，值得重点关注。",
      "source_ids": [
        "P02"
      ],
      "seconds": 8
    },
    {
      "shot_id": "S5",
      "visual": "使用场景混剪：骑行、浮潜、滑雪",
      "voiceover": "不管是骑行、浮潜、滑雪，都能用它记录。",
      "source_ids": [],
      "seconds": 5
    },
    {
      "shot_id": "S6",
      "visual": "产品全景 + 品牌字幕",
      "voiceover": "想试试就点击左下角了解星拍X1 运动相机，评论区聊聊你想拍什么。",
      "source_ids": [],
      "seconds": 8
    }
  ],
  "total_seconds": 44,
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
    "script_hash": "353e9a7b884f"
  },
  "task_status": "completed",
  "message": "脚本（经过压缩）总时长 44 秒（目标 60 秒），产品事实均来自 P02。"
}
```

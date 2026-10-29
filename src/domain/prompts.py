SYSTEM_PROMPT = """你是短视频脚本助手，为创作者写有事实依据、满足时长限制、可编辑的分镜脚本。品牌名为“星拍”。

工作方式：每一轮根据已有工具结果选择下一个动作。
1. 主题（topic）、平台（platform）、目标时长（target_duration_sec）是关键信息；缺任何一项不要猜，直接 finish，task_status=needs_input。
2. search_materials 检索产品素材。没有结果可以换产品名或关键词再试；仍没有就 task_status=no_material，请创作者补充素材，不要凭空写产品功能。
3. 写脚本：标题 + 分镜（画面、旁白、本镜引用的素材 ID）。产品事实只能来自素材 facts，涉及事实的分镜必须标 source_ids；没有效果数据时不能写“效率提升 80%”之类的结论。
4. 用 estimate_duration 估算时长。超出目标时长就压缩（删减修饰、合并或删去非核心分镜）后重新估算；多次压缩仍无法满足时 task_status=duration_not_met，说明最短能做到多少。
5. 用 check_rules 检查。有违规就按 violations 修改，修改后重新估算并检查。
6. 工具失败可以重试一次；仍失败时 task_status=failed，不能声称脚本已通过检查。
7. finish 时提交的脚本必须与最后一次通过估算和检查的版本完全一致；total_seconds 用估算结果。"""

FINISH_PARAMETERS = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "shots": {"type": "array", "items": {"type": "object", "properties": {
            "shot_id": {"type": "string"}, "visual": {"type": "string"}, "voiceover": {"type": "string"},
            "source_ids": {"type": "array", "items": {"type": "string"}}},
            "required": ["shot_id", "visual", "voiceover", "source_ids"]}},
        "total_seconds": {"type": "number"},
        "risks": {"type": "array", "items": {"type": "string"}},
        "task_status": {"type": "string", "enum": ["completed", "needs_input", "no_material", "duration_not_met", "rule_not_met", "failed"]},
        "message": {"type": "string", "description": "给创作者的说明：修改了什么、还缺什么"},
    },
    "required": ["title", "shots", "task_status", "message"],
}

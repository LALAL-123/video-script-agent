"""业务工具（本地函数 + 合成素材）：素材检索、时长估算、规则检查。

脚本本身由模型写（作为工具参数传入）。估算与检查都会返回 script_hash，
护栏据此确认最终提交的脚本正是通过了检查的那一版。
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import re
from pathlib import Path

from ..core.tools import Tool

DATA = Path(__file__).resolve().parents[2] / "data"
NUM = re.compile(r"(?<![A-Za-z])\d+(?:\.\d+)?%?")  # 不把 X1 这类型号当数字


def load_json(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def script_hash(title: str, shots: list) -> str:
    canon = {"title": title.strip(), "shots": [{"visual": s.get("visual", "").strip(), "voiceover": s.get("voiceover", "").strip(),
                                                 "source_ids": sorted(s.get("source_ids") or [])} for s in shots]}
    return hashlib.sha256(json.dumps(canon, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:12]


def shot_seconds(voiceover: str, cfg: dict) -> int:
    chars = len(re.sub(r"[^0-9a-zA-Z一-鿿]", "", voiceover))
    return math.ceil(chars / cfg["chars_per_second"]) + cfg["shot_overhead_seconds"]


def build_tools(request: dict, env: dict, store_dir: Path) -> list[Tool]:
    materials = {m["material_id"]: m for m in copy.deepcopy(load_json("materials.json")) + env.get("extra_materials", [])}
    for mid in env.get("remove_materials", []):
        materials.pop(mid, None)
    cfg = load_json("brand_rules.json")
    banned = cfg["rules"][0]["banned_terms"]
    target = request.get("target_duration_sec")

    def _validate(shots):
        if not isinstance(shots, list) or not shots:
            raise ValueError("shots 必须是非空数组")
        for s in shots:
            if not isinstance(s, dict) or "voiceover" not in s:
                raise ValueError("每个分镜需要 voiceover 字段")

    def search_materials(query: str):
        q = query.lower()
        hits = [m for m in materials.values()
                if any(k.lower() in q for k in m["keywords"]) or m["product"].lower() in q]
        return {"query": query, "count": len(hits),
                "materials": [{"material_id": m["material_id"], "product": m["product"], "facts": m["facts"],
                               "pain_point": m["pain_point"], "scenes": m["scenes"]} for m in hits],
                "note": "只能使用 facts 中的产品事实" if hits else "没有匹配素材"}

    def estimate_duration(title: str, shots: list):
        _validate(shots)
        per = [{"shot_id": s.get("shot_id", f"S{i + 1}"), "seconds": shot_seconds(s["voiceover"], cfg)} for i, s in enumerate(shots)]
        total = sum(p["seconds"] for p in per)
        result = {"script_hash": script_hash(title, shots), "total_seconds": total, "target_seconds": target, "shots": per,
                  "method": f"每 {cfg['chars_per_second']} 字 1 秒 + 每镜 {cfg['shot_overhead_seconds']} 秒转场"}
        if target:
            result["within_target"] = total <= target
            result["over_by_seconds"] = max(0, total - target)
            result["too_short"] = total < target * cfg["min_ratio_of_target"]
        return result

    def check_rules(title: str, shots: list):
        _validate(shots)
        violations = []
        texts = [("标题", title, [])] + [(s.get("shot_id", f"S{i + 1}"), s["voiceover"], s.get("source_ids") or [])
                                        for i, s in enumerate(shots)]
        for where, text, sources in texts:
            for w in banned:
                if w in text:
                    violations.append({"rule_id": "B01", "where": where, "detail": f"含绝对化用语“{w}”"})
            unknown = [x for x in sources if x not in materials]
            if unknown:
                violations.append({"rule_id": "B03", "where": where, "detail": f"素材 ID 不存在：{unknown}"})
            facts = " ".join(f for x in sources if x in materials for f in materials[x]["facts"])
            if where == "标题":
                facts = " ".join(f for s in shots for x in (s.get("source_ids") or []) if x in materials for f in materials[x]["facts"])
            for n in NUM.findall(text):
                if n not in facts:
                    violations.append({"rule_id": "B02", "where": where, "detail": f"数字“{n}”不在所引素材事实中"})
        if not any(cfg["brand"] in t for _, t, _ in texts):
            violations.append({"rule_id": "B04", "where": "全文", "detail": f"未出现品牌名“{cfg['brand']}”"})
        if len(title) > 30:
            violations.append({"rule_id": "B05", "where": "标题", "detail": f"标题 {len(title)} 字，超过 30 字"})
        return {"script_hash": script_hash(title, shots), "passed": not violations, "violations": violations}

    shot_schema = {"type": "object", "properties": {
        "shot_id": {"type": "string"}, "visual": {"type": "string", "description": "画面"},
        "voiceover": {"type": "string", "description": "旁白/字幕"},
        "source_ids": {"type": "array", "items": {"type": "string"}, "description": "本镜引用的素材 ID；不涉及产品事实可为空"}},
        "required": ["shot_id", "visual", "voiceover", "source_ids"]}
    script_params = {"type": "object", "properties": {"title": {"type": "string"},
                                                      "shots": {"type": "array", "items": shot_schema}},
                     "required": ["title", "shots"]}
    return [
        Tool("search_materials", "按产品名或关键词检索产品素材，返回素材 ID 与可用的产品事实。count=0 表示没有匹配素材。",
             {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}, search_materials),
        Tool("estimate_duration", "估算脚本时长（按旁白字数），返回每镜秒数、总时长、是否超出目标时长。", script_params, estimate_duration),
        Tool("check_rules", "按品牌规则 B01–B05 检查脚本：绝对化用语、无出处数字、素材 ID、品牌名、标题长度。", script_params, check_rules),
    ]

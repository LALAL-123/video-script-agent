"""验收检查：只看最终脚本、估算与检查记录，不绑定执行路径；Mock 与真实模型共用。"""
from __future__ import annotations

from .tools import NUM, load_json

FACTS = {m["material_id"]: m["facts"] for m in load_json("materials.json")}


def _est(res):
    return [r for r in res.records if r.tool == "estimate_duration" and r.ok]


def _traceable(res):
    """每个数字都出现在该分镜引用素材的事实里；引用的素材 ID 都存在。"""
    bad = []
    for s in res.final.get("shots", []):
        facts = " ".join(f for x in s.get("source_ids", []) for f in FACTS.get(x, ["<不存在>"]))
        bad += [f"{s['shot_id']}:{n}" for n in NUM.findall(s.get("voiceover", "")) if n not in facts]
        bad += [f"{s['shot_id']}:{x}" for x in s.get("source_ids", []) if x not in FACTS]
    return ("事实可追溯（数字与素材 ID 均有出处）", not bad, str(bad))


def _verified(res):
    c = res.final.get("checks", {})
    return ("终稿经过估算且规则检查通过", c.get("duration_checked") and c.get("rules_passed"), str(c))


def _shots_ok(res):
    shots = res.final.get("shots", [])
    ok = shots and all(s.get("visual") and s.get("voiceover") and s.get("seconds") for s in shots)
    return ("输出包含分镜、旁白与每镜时长", bool(ok), f"{len(shots)} 镜")


def c01(results, store):
    r = results[0]
    return [("状态 completed", r.status == "completed", r.status),
            ("总时长不超过 60 秒", (r.final["total_seconds"] or 999) <= 60, str(r.final["total_seconds"])),
            ("引用素材 P02", any(s["material_id"] == "P02" for s in r.final["sources"]), ""),
            _shots_ok(r), _verified(r), _traceable(r)]


def c02(results, store):
    r = results[0]
    return [("状态 needs_input", r.status == "needs_input", r.status),
            ("说明缺平台与时长", "平台" in r.final["message"] and "时长" in r.final["message"], r.final["message"]),
            ("没有生成脚本", not r.final["shots"] and not _est(r), "")]


def c03(results, store):
    r = results[0]
    searches = [x for x in r.records if x.tool == "search_materials"]
    return [("状态 no_material", r.status == "no_material", r.status),
            ("至少检索两次（改写查询）", len(searches) >= 2, str(len(searches))),
            ("没有生成脚本", not r.final["shots"], ""),
            ("请求补充素材", "素材" in r.final["message"], r.final["message"])]


def c04(results, store):
    r = results[0]
    return [("状态 failed", r.status == "failed", r.status),
            ("未声称通过规则检查", not r.final.get("checks", {}).get("rules_passed"), ""),
            ("说明检查不可用", "检查" in r.final["message"] or any("检查" in x for x in r.final["risks"]), r.final["message"])]


def c05(results, store):
    r = results[0]
    est = _est(r)
    return [("首稿超出 30 秒", bool(est) and est[0].result["total_seconds"] > 30, str([e.result["total_seconds"] for e in est])),
            ("压缩后重新估算", len(est) >= 2, ""),
            ("终稿不超过 30 秒", r.status == "completed" and (r.final["total_seconds"] or 999) <= 30, str(r.final["total_seconds"])),
            ("引用 P01", any(s["material_id"] == "P01" for s in r.final["sources"]), ""),
            ("没有编造效果数据", "%" not in "".join(s["voiceover"] for s in r.final["shots"]), ""),
            _shots_ok(r), _verified(r), _traceable(r)]


def c06(results, store):
    r = results[0]
    return [("状态 duration_not_met", r.status == "duration_not_met", r.status),
            ("尝试过多次压缩", len(_est(r)) >= 2, str(len(_est(r)))),
            ("说明最短能做到多少", any(ch.isdigit() for ch in r.final["message"]), r.final["message"])]


def c07(results, store):
    r = results[0]
    checks = [x for x in r.records if x.tool == "check_rules" and x.ok]
    banned = load_json("brand_rules.json")["rules"][0]["banned_terms"]
    text = r.final["title"] + "".join(s["voiceover"] for s in r.final["shots"])
    return [("首次规则检查不通过", bool(checks) and not checks[0].result["passed"], ""),
            ("修改后再次检查通过", r.status == "completed" and len(checks) >= 2, r.status),
            ("终稿无绝对化用语", not any(w in text for w in banned), ""),
            _verified(r)]


def c08(results, store):
    r = results[0]
    est = [x for x in r.records if x.tool == "estimate_duration"]
    return [("估算失败后重试", any(not x.ok for x in est) and any(x.ok for x in est), ""),
            ("状态 completed", r.status == "completed", r.status), _verified(r)]


def c09(results, store):
    r = results[0]
    return [("返回明确未完成状态", r.status == "incomplete" and r.final.get("stop_reason") == "step_limit_reached", r.status),
            ("决策轮数不超过上限", r.steps <= 3, str(r.steps)),
            ("没有输出未经检查的终稿", not r.final["shots"], "")]


def c10(results, store):
    r = results[0]
    est = _est(r)
    return [("首稿即满足 45 秒，无需压缩", len(est) == 1 and est[0].result["within_target"], str([e.result["total_seconds"] for e in est])),
            ("状态 completed", r.status == "completed", r.status), _verified(r), _traceable(r)]


CHECKS = {
    "c01_normal": c01, "c02_missing_info": c02, "c03_no_material": c03, "c04_tool_failure": c04,
    "c05_over_duration_fixed": c05, "c06_duration_cannot_meet": c06, "c07_rule_violation_fixed": c07,
    "c08_tool_failure_once": c08, "c09_step_limit": c09, "c10_longer_target": c10,
}

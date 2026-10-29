"""结束护栏：最终脚本必须正是通过了时长估算和规则检查的那一版。

用 script_hash 把 finish 提交的脚本与估算、检查记录对应起来：
没估算过、超时长、没检查过或检查未通过的脚本不能标为 completed；
总时长以估算结果为准；引用的素材必须是本轮检索到的。
"""
from __future__ import annotations

from ..core.agent import ToolRecord
from .tools import script_hash


def guard(args: dict, records: list[ToolRecord], payload: dict) -> tuple[dict, list[str]]:
    shots = args.get("shots")
    if not isinstance(shots, list):
        raise ValueError("finish.shots 必须是数组")
    fixes: list[str] = []
    title = str(args.get("title") or "")
    status = args.get("task_status")
    searched = {m["material_id"]: m for r in records if r.tool == "search_materials" and r.ok for m in r.result["materials"]}
    estimates = {r.result["script_hash"]: r.result for r in records if r.tool == "estimate_duration" and r.ok}
    checks = {r.result["script_hash"]: r.result for r in records if r.tool == "check_rules" and r.ok}
    h = script_hash(title, shots) if shots else None
    est, chk = estimates.get(h), checks.get(h)

    missing = [k for k in ("topic", "platform", "target_duration_sec") if not payload.get(k)]
    bad_sources = sorted({x for s in shots for x in (s.get("source_ids") or []) if x not in searched})
    if bad_sources:
        fixes.append(f"分镜引用了未检索到的素材 {bad_sources}")

    if missing:
        new = "needs_input"
    elif status == "completed":
        if not searched:
            new = "no_material"
        elif est is None:
            new = "unverified"
            fixes.append("最终脚本没有经过时长估算（与估算过的版本不一致）")
        elif not est.get("within_target", True):
            new = "duration_not_met"
            fixes.append(f"最终脚本 {est['total_seconds']} 秒，超过目标 {est['target_seconds']} 秒")
        elif chk is None:
            checks_tried = [r for r in records if r.tool == "check_rules"]
            new = "failed" if checks_tried and not any(r.ok for r in checks_tried) else "unverified"
            fixes.append("最终脚本没有通过规则检查记录（检查失败或版本不一致）")
        elif not chk["passed"]:
            new = "rule_not_met"
            fixes.append("最终脚本的规则检查未通过")
        elif bad_sources:
            new = "unverified"
        else:
            new = "completed"
    else:
        new = status
    if new != status:
        fixes.append(f"task_status 由 {status} 校正为 {new}")

    total = est["total_seconds"] if est else None
    if args.get("total_seconds") not in (None, total) and shots:
        fixes.append(f"total_seconds 以估算为准：{args.get('total_seconds')} → {total}")
    per = {p["shot_id"]: p["seconds"] for p in (est or {}).get("shots", [])}
    risks = list(args.get("risks") or [])
    if chk and not chk["passed"]:
        risks += [f"{v['rule_id']} {v['where']}：{v['detail']}" for v in chk["violations"]]
    if est and est.get("too_short"):
        risks.append(f"总时长 {est['total_seconds']} 秒，明显短于目标")
    used = sorted({x for s in shots for x in (s.get("source_ids") or []) if x in searched})
    final = {
        "title": title,
        "shots": [{**s, "seconds": per.get(s.get("shot_id"))} for s in shots],
        "total_seconds": total,
        "target_seconds": payload.get("target_duration_sec"),
        "sources": [{"material_id": m, "product": searched[m]["product"], "facts": searched[m]["facts"]} for m in used],
        "risks": risks,
        "checks": {"duration_checked": est is not None, "rules_checked": chk is not None,
                   "rules_passed": bool(chk and chk["passed"]), "script_hash": h},
        "task_status": new,
        "message": str(args.get("message") or ""),
    }
    return final, fixes


def on_incomplete(records: list[ToolRecord], payload: dict, reason: str) -> dict:
    est = [r.result["total_seconds"] for r in records if r.tool == "estimate_duration" and r.ok]
    return {"title": "", "shots": [], "total_seconds": None, "target_seconds": payload.get("target_duration_sec"),
            "sources": [], "checks": {"duration_checked": False, "rules_checked": False, "rules_passed": False},
            "estimates_seconds": est, "risks": [],
            "message": f"未完成：{reason}；已估算 {len(est)} 版脚本，未形成通过检查的终稿。"}

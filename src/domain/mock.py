"""离线 Mock 策略：确定性规则，读取工具结果后选择下一步。

脚本由模板拼出，有三档详略（0 最详细、2 最精简）：估算超时就降一档重写，
检查出违规就删掉违规词再检查。只用于无模型时验证循环、工具、护栏与 Trace，
不代表真实模型的写作和修改能力。
"""
from __future__ import annotations

from ..core.llm import Observation

BRAND = "星拍"
HYPE = "史上最强的"  # “夸张”风格首稿会带上它，用来演示规则检查不通过后的修改


def compose(materials: list[dict], req: dict, level: int, clean: bool) -> dict:
    m = materials[0]
    product = m["product"]
    hype = HYPE if ("夸张" in (req.get("style") or "") and not clean) else ""
    hook = {
        0: f"你是不是也有这种烦恼：{m['pain_point']}，折腾半天效果还是不满意？今天带你看看{hype}{product}。",
        1: f"{m['pain_point']}？折腾半天还不满意？看看{hype}{product}。",
        2: f"{m['pain_point']}？试试{hype}{product}。",
    }[level]
    shots = [{"shot_id": "S1", "visual": "创作者面对镜头提出痛点", "voiceover": hook, "source_ids": []}]
    for mm in materials:
        for fact in mm["facts"]:
            vo = {0: f"先说最实用的一点，{mm['product']}{fact}，日常拍摄的时候真的省心不少，建议大家重点关注。",
                  1: f"{mm['product']}{fact}，日常拍摄省心不少，值得重点关注。",
                  2: f"{mm['product']}{fact}。"}[level]
            shots.append({"shot_id": f"S{len(shots) + 1}", "visual": f"产品特写：{fact}", "voiceover": vo,
                          "source_ids": [mm["material_id"]]})
    if level < 2:
        scenes = "、".join(m["scenes"])
        vo = f"不管是{scenes}，都可以带上它记录下来。" if level == 0 else f"不管是{scenes}，都能用它记录。"
        shots.append({"shot_id": f"S{len(shots) + 1}", "visual": f"使用场景混剪：{scenes}", "voiceover": vo, "source_ids": []})
    cta = {0: f"想试试的话，点击左下角了解{BRAND}{product}，评论区告诉我你想用它拍什么。",
           1: f"想试试就点击左下角了解{BRAND}{product}，评论区聊聊你想拍什么。", 2: f"了解{BRAND}{product}。"}[level]
    shots.append({"shot_id": f"S{len(shots) + 1}", "visual": "产品全景 + 品牌字幕", "voiceover": cta, "source_ids": []})
    return {"title": f"{BRAND}{product}：{m['pain_point'][:8]}的解法", "shots": shots}


def _ok(o):
    return o is not None and o.result.get("ok")


def _finish(note, status, script=None, total=None, risks=(), message=""):
    script = script or {"title": "", "shots": []}
    return "finish", note, {**script, "total_seconds": total, "risks": list(risks), "task_status": status, "message": message}


def mock_policy(payload: dict, obs: list[Observation]):
    names = {"topic": "主题", "platform": "平台", "target_duration_sec": "目标时长"}
    missing = [n for k, n in names.items() if not payload.get(k)]
    if missing:
        return _finish("关键信息缺失，不猜测", "needs_input", message=f"请补充：{'、'.join(missing)}。")
    target = payload["target_duration_sec"]

    searches = [o for o in obs if o.tool == "search_materials"]
    if not searches:
        return "search_materials", f"按主题“{payload['topic']}”检索产品素材", {"query": payload["topic"]}
    if not _ok(searches[-1]) and not any(_ok(s) and s.result["count"] for s in searches):
        if len(searches) < 2:
            return "search_materials", f"检索失败（{searches[-1].result.get('error')}），重试一次", searches[-1].args
        return _finish("素材检索连续失败", "failed", message="素材服务不可用，未生成脚本。")
    hit = next((s for s in reversed(searches) if _ok(s) and s.result["count"] > 0), None)
    if hit is None:
        alt = payload.get("product") or payload["topic"].split()[-1]
        if len(searches) < 2 and alt != searches[-1].args.get("query"):
            return "search_materials", f"主题检索无结果，改用产品词“{alt}”再试", {"query": alt}
        return _finish("两次检索都没有素材，不能凭空写产品事实", "no_material",
                       message=f"素材库里没有“{payload['topic']}”的产品素材，请补充产品事实后再生成。")
    materials = hit.result["materials"][:1]

    estimates = [o for o in obs if o.tool == "estimate_duration"]
    checks = [o for o in obs if o.tool == "check_rules"]
    over = sum(1 for e in estimates if _ok(e) and not e.result["within_target"])
    clean = any(_ok(c) and not c.result["passed"] for c in checks)
    level = min(over, 2)
    script = compose(materials, payload, level, clean)

    est = next((e for e in reversed(estimates) if e.args == script), None)
    if est is None or not _ok(est):
        tries = [e for e in estimates if e.args == script]
        if len(tries) >= 2:
            return _finish("时长估算连续失败", "failed", script, message="时长估算服务不可用，脚本未经校验。")
        if not estimates:
            note = "首稿完成，估算时长"
        elif tries:
            note = f"估算失败（{tries[-1].result.get('error')}），重试一次"
        elif clean and level == min(over, 2):
            note = "已按规则检查结果删除违规用语，重新估算"
        else:
            note = f"上一版超出目标 {estimates[-1].result.get('over_by_seconds')} 秒，压缩后重新估算"
        return "estimate_duration", note, script
    if not est.result["within_target"]:
        return _finish("已压缩到最精简版本仍超出目标时长", "duration_not_met", script, est.result["total_seconds"],
                       message=f"最精简版本 {est.result['total_seconds']} 秒，仍超过目标 {target} 秒；建议放宽时长或减少要讲的卖点。")

    chk = next((c for c in reversed(checks) if c.args == script), None)
    if chk is None or not _ok(chk):
        tries = [c for c in checks if c.args == script]
        if len(tries) >= 2:
            return _finish("规则检查连续失败，不能声称合规", "failed", script, est.result["total_seconds"],
                           ["规则检查未完成"], "时长已满足，但规则检查服务不可用，脚本未通过合规校验，请稍后重试。")
        note = "时长满足目标，进行规则检查" if not tries else f"规则检查失败（{tries[-1].result.get('error')}），重试一次"
        return "check_rules", note, script
    if not chk.result["passed"]:
        if clean:  # 已经清理过仍不通过
            return _finish("修改后仍有违规", "rule_not_met", script, est.result["total_seconds"],
                           [v["detail"] for v in chk.result["violations"]], "规则检查未通过，需人工修改。")
        return "estimate_duration", "规则检查不通过，删除违规用语后重新估算", compose(materials, payload, level, True)
    revised = "（经过压缩）" if over else ""
    return _finish("时长与规则检查均通过", "completed", script, est.result["total_seconds"],
                   message=f"脚本{revised}总时长 {est.result['total_seconds']} 秒（目标 {target} 秒），产品事实均来自 {materials[0]['material_id']}。")

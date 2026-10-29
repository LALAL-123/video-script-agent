"""题 4 业务工具与护栏测试。"""
from pathlib import Path

import pytest

from src import domain
from src.core.agent import ToolRecord
from src.core.llm import ScriptedLLM
from src.core.runner import check_case, load_case, run_case
from src.domain.tools import build_tools, script_hash

CASES = sorted((Path(__file__).resolve().parent.parent / "examples" / "cases").glob("*.json"))
REQ = {"topic": "快剪 App", "platform": "抖音", "target_duration_sec": 30}
SHOTS = [{"shot_id": "S1", "visual": "演示", "voiceover": "星拍快剪 App 支持字幕。", "source_ids": ["P01"]}]


def tools(tmp_path, request=REQ):
    return {t.name: t.fn for t in build_tools(request=request, env={}, store_dir=tmp_path)}


def test_search_returns_only_facts_from_materials(tmp_path):
    r = tools(tmp_path)["search_materials"]("快剪 App 自动字幕")
    assert r["count"] == 1 and r["materials"][0]["facts"] == ["支持字幕"]
    assert tools(tmp_path)["search_materials"]("智能手表")["count"] == 0


def test_estimate_reports_overrun(tmp_path):
    long = [{**SHOTS[0], "voiceover": "字" * 200}]
    r = tools(tmp_path)["estimate_duration"]("t", long)
    assert r["within_target"] is False and r["over_by_seconds"] > 0


def test_rules_catch_fabricated_numbers_banned_words_and_unknown_ids(tmp_path):
    bad = [{"shot_id": "S1", "visual": "v", "voiceover": "星拍快剪效率提升 80%，史上最强", "source_ids": ["P01", "P99"]}]
    v = {x["rule_id"] for x in tools(tmp_path)["check_rules"]("标题", bad)["violations"]}
    assert {"B01", "B02", "B03"} <= v


def test_rules_accept_model_name_and_supported_numbers(tmp_path):
    ok = [{"shot_id": "S1", "visual": "v", "voiceover": "星拍 X1 运动相机支持 4K 60 帧录制", "source_ids": ["P02"]}]
    assert tools(tmp_path)["check_rules"]("X1 骑行记录", ok)["passed"] is True


def rec(tool, result):
    return ToolRecord(1, tool, {}, {"ok": True, **result})


SEARCH = rec("search_materials", {"materials": [{"material_id": "P01", "product": "快剪 App", "facts": ["支持字幕"]}]})
H = script_hash("标题", SHOTS)


def finish(shots=SHOTS, total=6):
    return {"title": "标题", "shots": shots, "total_seconds": total, "task_status": "completed", "message": ""}


def test_guard_requires_final_script_to_match_checked_version():
    recs = [SEARCH, rec("estimate_duration", {"script_hash": H, "total_seconds": 6, "within_target": True, "shots": []}),
            rec("check_rules", {"script_hash": H, "passed": True, "violations": []})]
    final, fixes = domain.guard(finish(), recs, REQ)
    assert final["task_status"] == "completed" and not fixes
    edited = [{**SHOTS[0], "voiceover": "星拍快剪 App 支持字幕，效率提升 80%。"}]
    final, fixes = domain.guard(finish(edited), recs, REQ)
    assert final["task_status"] == "unverified" and fixes


def test_guard_blocks_overlong_and_unchecked_scripts():
    over = [SEARCH, rec("estimate_duration", {"script_hash": H, "total_seconds": 38, "target_seconds": 30, "within_target": False, "shots": []})]
    assert domain.guard(finish(total=28), over, REQ)[0]["task_status"] == "duration_not_met"
    fine = [SEARCH, rec("estimate_duration", {"script_hash": H, "total_seconds": 6, "within_target": True, "shots": []}),
            ToolRecord(1, "check_rules", {}, {"ok": False, "error": "503"})]
    final, _ = domain.guard(finish(), fine, REQ)
    assert final["task_status"] == "failed" and final["total_seconds"] == 6


@pytest.mark.parametrize("path", CASES, ids=lambda p: p.stem)
def test_case_acceptance_with_offline_mock(path, tmp_path):
    case = load_case(path)
    outputs = run_case(case, domain, ScriptedLLM(domain.mock_policy), tmp_path)
    checks = check_case(case, domain, [r for _, r in outputs], tmp_path)
    assert checks and all(c["ok"] for c in checks), [c for c in checks if not c["ok"]]

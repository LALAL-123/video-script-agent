# 验收结果（mock:scripted-policy）

检查通过 41/41。逐条 Trace 见 `examples/runs/mock/`。

| 用例 | 覆盖验收点 | 结束状态 | 检查通过 |
|---|---|---|---|
| c01_normal | 正常生成 | completed | 6/6 |
| c02_missing_info | 缺关键信息 | needs_input | 3/3 |
| c03_no_material | 无素材 | no_material | 4/4 |
| c04_tool_failure | 工具失败 | failed | 3/3 |
| c05_over_duration_fixed | 超时长后的修正、正常生成 | completed | 8/8 |
| c06_duration_cannot_meet | 超时长后的明确失败 | duration_not_met | 3/3 |
| c07_rule_violation_fixed | 正常生成 | completed | 4/4 |
| c08_tool_failure_once | 工具失败 | completed | 3/3 |
| c09_step_limit | 步数上限 | incomplete | 3/3 |
| c10_longer_target | 正常生成 | completed | 4/4 |

## 未通过的检查

无

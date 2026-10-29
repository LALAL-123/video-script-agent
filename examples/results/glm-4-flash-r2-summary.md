# 验收结果（openai-compat:glm-4-flash）

检查通过 20/41。逐条 Trace 见 `examples/runs/glm-4-flash-r2/`。

| 用例 | 覆盖验收点 | 结束状态 | 检查通过 |
|---|---|---|---|
| c01_normal | 正常生成 | unverified | 2/6 |
| c02_missing_info | 缺关键信息 | needs_input | 1/3 |
| c03_no_material | 无素材 | no_material | 4/4 |
| c04_tool_failure | 工具失败 | unverified | 1/3 |
| c05_over_duration_fixed | 超时长后的修正、正常生成 | unverified | 4/8 |
| c06_duration_cannot_meet | 超时长后的明确失败 | unverified | 0/3 |
| c07_rule_violation_fixed | 正常生成 | rule_not_met | 2/4 |
| c08_tool_failure_once | 工具失败 | rule_not_met | 1/3 |
| c09_step_limit | 步数上限 | incomplete | 3/3 |
| c10_longer_target | 正常生成 | rule_not_met | 2/4 |

## 未通过的检查

- c01_normal：状态 completed（unverified）
- c01_normal：总时长不超过 60 秒（None）
- c01_normal：输出包含分镜、旁白与每镜时长（5 镜）
- c01_normal：终稿经过估算且规则检查通过（{'duration_checked': False, 'rules_checked': False, 'rules_passed': False, 'script_hash': '45e60c2cddd2'}）
- c02_missing_info：说明缺平台与时长（脚本已撰写完毕，请查看）
- c02_missing_info：没有生成脚本（）
- c04_tool_failure：状态 failed（unverified）
- c04_tool_failure：说明检查不可用（脚本已根据素材信息完成撰写，请查看。）
- c05_over_duration_fixed：首稿超出 30 秒（[24]）
- c05_over_duration_fixed：压缩后重新估算（）
- c05_over_duration_fixed：终稿不超过 30 秒（24）
- c05_over_duration_fixed：终稿经过估算且规则检查通过（{'duration_checked': True, 'rules_checked': False, 'rules_passed': False, 'script_hash': 'fc2fc5e49249'}）
- c06_duration_cannot_meet：状态 duration_not_met（unverified）
- c06_duration_cannot_meet：尝试过多次压缩（0）
- c06_duration_cannot_meet：说明最短能做到多少（脚本已撰写完毕，符合要求）
- c07_rule_violation_fixed：修改后再次检查通过（rule_not_met）
- c07_rule_violation_fixed：终稿经过估算且规则检查通过（{'duration_checked': True, 'rules_checked': True, 'rules_passed': False, 'script_hash': '9680554c1286'}）
- c08_tool_failure_once：状态 completed（rule_not_met）
- c08_tool_failure_once：终稿经过估算且规则检查通过（{'duration_checked': True, 'rules_checked': True, 'rules_passed': False, 'script_hash': 'be716c6e93e7'}）
- c10_longer_target：状态 completed（rule_not_met）
- c10_longer_target：终稿经过估算且规则检查通过（{'duration_checked': True, 'rules_checked': True, 'rules_passed': False, 'script_hash': 'be716c6e93e7'}）

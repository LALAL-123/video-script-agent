# 03 评估

## 测试结构

| 层次 | 文件 | 内容 |
|---|---|---|
| 内核 | `tests/test_core.py` | 步数/调用上限、finish 同轮拒绝、工具异常转观察、故障注入、模型异常、非法 finish 退回 |
| 业务 | `tests/test_domain.py` | 检索只返回给定事实、超时判断、规则捕获编造数字/绝对化用语/未知 ID、型号不误判、护栏拦截改过未检查的终稿、超时与检查失败 |
| 验收 | `tests/test_domain.py::test_case_acceptance_with_offline_mock` | 10 个用例逐条跑验收检查 |
| 评估 | `python -m src.cli eval --llm mock|openai` | 同一套检查用于 Mock 与真实模型 |

验收检查（`src/domain/checks.py`）中“事实可追溯”一条独立于 `check_rules`：直接用素材原始事实逐镜核对旁白中的数字与素材 ID。

## 用例：预期与实际（离线 Mock）

全部结果：[examples/results/mock-summary.md](../examples/results/mock-summary.md)，测试输出：[examples/results/pytest.txt](../examples/results/pytest.txt)。

| 用例 | 预期 | 实际 | Trace |
|---|---|---|---|
| c01 正常生成 | X1 60 秒，首稿通过估算与检查，引用 P02 | 一致，6/6 | [c01](../examples/runs/mock/c01_normal.md) |
| c02 缺关键信息 | needs_input，说明缺平台与时长，不写脚本 | 一致，3/3 | [c02](../examples/runs/mock/c02_missing_info.md) |
| c03 无素材 | 改写检索后仍无 → no_material，请补充素材 | 一致，4/4 | [c03](../examples/runs/mock/c03_no_material.md) |
| c04 规则检查持续失败 | failed，不声称合规 | 一致，3/3 | [c04](../examples/runs/mock/c04_tool_failure.md) |
| c05 超时长修正（参考实例） | 首稿 38 秒 > 30 → 压缩 → 29 秒，检查通过，引用 P01，无编造数据 | 一致，8/8 | [c05](../examples/runs/mock/c05_over_duration_fixed.md) |
| c06 压不进时长 | 38 → 29 → 12 秒仍 > 8 → duration_not_met，说明最短时长 | 一致，3/3 | [c06](../examples/runs/mock/c06_duration_cannot_meet.md) |
| c07 规则违规修正 | 首次检查含“史上/最强”不通过 → 修改 → 再查通过 | 一致，4/4 | [c07](../examples/runs/mock/c07_rule_violation_fixed.md) |
| c08 估算失败一次 | 重试后完成 | 一致，3/3 | [c08](../examples/runs/mock/c08_tool_failure_once.md) |
| c09 步数上限 | 3 轮后 incomplete，无终稿 | 一致，3/3 | [c09](../examples/runs/mock/c09_step_limit.md) |
| c10 目标 45 秒（c05 对照） | 首稿 38 秒即满足，只估算一次 | 一致，4/4 | [c10](../examples/runs/mock/c10_longer_target.md) |

参考实例给出的修正结果是 28 秒；本实现的估算口径下压缩稿为 29 秒，同样满足“≤ 30 秒”。Mock 运行中护栏校正次数为 0；护栏拦截能力由 `test_guard_*` 单测验证。

## 真实模型

模型：智谱 GLM-4-Flash（免费版，OpenAI 兼容接口，temperature=0）。与 Mock 共用同一套检查。

| 轮次 | 代码 | 检查通过 | 护栏校正 | 汇总 | Trace |
|---|---|---|---|---|---|
| 第 1 轮 | 初版 | 评估中断 | — | 无汇总 | [c01](../examples/runs/glm-4-flash-r1/c01_normal.md) |
| 第 2 轮 | 按第 1 轮问题修改 | 20/41 | 17 | [r2 汇总](../examples/results/glm-4-flash-r2-summary.md) | [glm-4-flash-r2/](../examples/runs/glm-4-flash-r2/) |

### 第 1 轮暴露的问题与修改

| 现象（第 1 轮） | 修改（第 2 轮运行前完成） |
|---|---|
| c01 中模型把 finish 写成文本，循环一直拿不到调用，到上限 incomplete | 内核：文本中写明工具名且紧跟 JSON 参数时恢复为调用，Trace 标注“从文本恢复” |
| incomplete 结果缺 `total_seconds`，检查抛 KeyError，整个评估中断 | 检查出错记为一条未通过的检查，不再中断；incomplete 结果补齐全部字段 |

第 2 轮有 5 个用例的第一个调用是从文本恢复的（c01、c03、c04、c06、c07）。

### 第 2 轮未通过项

主要现象只有一类：模型不调用 `estimate_duration` / `check_rules`，或者改稿后不重新估算、检查就 finish，并自报 completed。护栏用 `script_hash` 比对，终稿不是估算、检查过的版本，于是校正状态：

| 用例 | 模型自报 | 护栏校正后 | 检查期望 |
|---|---|---|---|
| c01 正常、c05 超时长修正 | completed | unverified | completed |
| c04 检查工具失败 | completed | unverified | failed（说明检查不可用） |
| c06 时长做不到 | completed | unverified | duration_not_met |
| c07 违规修正、c08 单次失败、c10 更长目标 | completed | rule_not_met | completed |
| c02 缺平台与时长 | completed，并直接写了脚本 | needs_input | needs_input 且不生成脚本 |

c03（无素材）与 c09（步数上限）通过。

### 结论

- 17 次护栏校正全部是把“未经核验的 completed”降级；没有一份未估算或未通过检查的脚本以 completed 交出。
- GLM-4-Flash 不会稳定地走“估算 → 检查 → 修改 → 复查”闭环。护栏现在是事后降级；更好的做法是像题 1 一样在 finish 时退回模型（终稿 hash 未经估算/检查就拒绝结束），把闭环交还给模型完成，降级只作为步数用尽时的兜底。
- 也可以把估算与规则检查合并成一个 `validate_script` 工具，减少弱模型需要记住的步骤。

## 失败与限制

- 离线 Mock 的脚本是模板拼的三档详略，它通过只说明流程与检查闭合，不证明真实模型的写作与压缩能力。
- c05 要求首稿超过 30 秒，这是为了复现参考实例；真实模型若首稿就写得很短，该条会失败但其余条目通过——说明它没有走到“修正”路径，需要另看 c06/c07。
- 无数字的夸大（“效率翻倍”除外的“超好用”等）只能靠绝对化用语表与模型自觉，未做语义核查。
- 时长估算不区分纯画面镜头与口播镜头。

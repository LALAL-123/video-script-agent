# 短视频脚本 Agent（题 4）

帮创作者生成**有事实依据、满足时长限制、可编辑**的分镜脚本：检索产品素材 → 写脚本（每镜标注素材 ID）→ 估算时长，超时就压缩再估 → 规则检查，违规就修改再查 → 提交通过检查的那一版。缺关键信息、无素材、工具失败、压不进时长都返回明确状态。

原生 Python 实现 ReAct 循环（模型选动作 → 执行工具 → 观察 → 再决策或结束），脚本由模型写在工具参数里；模型走 OpenAI 兼容接口，另有离线 Mock 入口，用于在无模型时验证流程。

## 评审入口

```bash
pip install -r requirements.txt
python -m pytest -q                                   # 内核 + 业务 + 10 个验收用例（离线）
python -m src.cli eval --llm mock                     # 跑全部用例，写出 Trace 与汇总
python -m src.cli run examples/cases/c05_over_duration_fixed.json --llm mock     # 参考实例
```

真实模型（任一 OpenAI 兼容服务；本仓库结果用智谱 GLM-4-Flash 免费版）：

```bash
cp .env.example .env        # 填 LLM_API_KEY、LLM_BASE_URL、LLM_MODEL
python -m src.cli eval --llm openai
```

| 想看什么 | 文件 |
|---|---|
| 验收汇总（Mock） | [examples/results/mock-summary.md](examples/results/mock-summary.md) |
| 参考实例：P01 30 秒，首稿 38 秒 → 压缩到 29 秒 | [examples/runs/mock/c05_over_duration_fixed.md](examples/runs/mock/c05_over_duration_fixed.md) |
| 同一素材目标 45 秒，无需压缩（对照） | [examples/runs/mock/c10_longer_target.md](examples/runs/mock/c10_longer_target.md) |
| 规则检查不通过 → 修改 → 再检查 | [examples/runs/mock/c07_rule_violation_fixed.md](examples/runs/mock/c07_rule_violation_fixed.md) |
| 压到最精简仍超时 → 明确失败 | [examples/runs/mock/c06_duration_cannot_meet.md](examples/runs/mock/c06_duration_cannot_meet.md) |
| 真实模型结果（GLM-4-Flash 第 2 轮） | [汇总](examples/results/glm-4-flash-r2-summary.md)，分析见 [docs/03-evaluation.md](docs/03-evaluation.md) |
| 测试输出 | [examples/results/pytest.txt](examples/results/pytest.txt) |

## 环境

- Python 3.10+（开发环境 3.13.4，Windows 11）
- 依赖：`openai`（仅真实模型需要）、`pytest`
- 环境变量见 [.env.example](.env.example)；Mock 模式无需配置

## 验收点与用例

| 验收点 | 用例（`examples/cases/`） |
|---|---|
| 正常生成 | `c01_normal`、`c10_longer_target`、`c07_rule_violation_fixed`（规则修正） |
| 缺关键信息 | `c02_missing_info` |
| 无素材 | `c03_no_material` |
| 工具失败 | `c04_tool_failure`（规则检查持续失败）、`c08_tool_failure_once`（估算失败一次后重试） |
| 超时长后的修正或明确失败 | `c05_over_duration_fixed`（参考实例）、`c06_duration_cannot_meet` |
| 步数上限 | `c09_step_limit` |

自己出题：复制用例改 `target_duration_sec` / `topic` / `style`，或在 `env.extra_materials` 里加素材、`env.remove_materials` 删素材、`faults` 注入故障。

## 目录

```
src/core/      与业务无关的 ReAct 内核：模型接入、循环、工具注册/故障注入、Trace、用例运行
src/domain/    本题业务：检索/估算/检查工具、提示词、结束护栏（终稿与检查版本一致）、离线 Mock 策略、验收检查
src/cli.py     命令行入口
data/          合成产品素材（只含给定事实）、品牌规则与时长估算参数
examples/      cases/ 输入；runs/ 实际输出与 Trace；results/ 汇总与测试输出
tests/         内核测试、业务测试、全部用例的验收测试
docs/          需求、方案、评估、AI 使用说明、复盘
```

## 已知限制

- `examples/runs/mock/` 是离线 Mock 的记录：Mock 的脚本是模板拼的三档详略，只证明流程、工具、护栏打通；真实的写作与修改能力以 `--llm openai` 的运行记录为准。
- 时长按“每 4.5 字 1 秒 + 每镜 1 秒转场”估算，不考虑语速风格与纯画面镜头。
- 事实核查只能机械检查数字和素材 ID；“效率翻倍”这类无数字的夸大说法要靠绝对化用语表和模型自觉。

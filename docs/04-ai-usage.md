# 04 AI 使用说明

## 使用的工具

- Claude Code（模型 Claude Opus 5.5），在本地仓库中生成代码、数据、用例与文档，运行测试与评估。
- 智谱 GLM-4-Flash（免费版）：作为智能体运行时的决策模型，用于真实模型评估，不参与写代码。

## AI 生成的内容

| 部分 | 内容 |
|---|---|
| `src/core/` | ReAct 循环、OpenAI 兼容接入、离线 Mock 适配、工具注册与故障注入、Trace 输出、用例运行 |
| `src/domain/` | 检索/时长估算/规则检查工具、系统提示词、结束护栏、Mock 策略（模板脚本）、验收检查 |
| `data/`、`examples/cases/` | 合成产品素材、品牌规则与 10 个用例 |
| `tests/` | 内核、业务、验收测试 |
| `docs/`、`README.md` | 初稿 |

## 本人的修改与决策

本人没有直接改写代码或提示词，所做的是以下决策：

- 让 AI 把四道题都实现出来，按真实模型结果再选题；根据评估对比选定提交题 2，本题作为对照一并公开。
- 选用免费、OpenAI 兼容的智谱 GLM-4-Flash 作为真实模型，自行申请 API Key，只放在本地 `.env`（已被 `.gitignore` 排除）。
- 要求在真实模型上多轮评估，并在文档中如实报告每轮结果与未通过项，不为过检查而改标准。
- 四个仓库均公开发布；通过 GitHub Desktop 推送，并在 GitHub 上统一改为英文仓库名。

## 开发中发现并修正的问题

以下问题由 AI 在阅读测试输出和真实模型 Trace 时发现并修正：

| 问题 | 修正 |
|---|---|
| GLM-4-Flash 常把工具调用写成文本，循环拿不到调用 | 内核只在文本写明工具名且紧跟 JSON 参数时恢复为调用，并在 Trace 中标注 |
| 某次结束结果缺字段时，检查抛异常导致整个评估中断 | 检查出错记为一条未通过的检查 |
| 未完成结果缺 `total_seconds` 等字段，第 1 轮评估在 c01 中断 | 未完成结果补齐全部字段 |
| 数字规则把型号“X1”中的 1 当成无出处的数字 | 数字匹配排除紧跟在字母后的数字 |
| 测试输出里带有本机用户路径 | 生成 `examples/results/pytest.txt` 时脱敏 |

## 验证方式

1. `python -m pytest -q`：全部通过（见 [examples/results/pytest.txt](../examples/results/pytest.txt)）。
2. `python -m src.cli eval --llm mock`：41/41 项检查通过（见 [examples/results/mock-summary.md](../examples/results/mock-summary.md)）。
3. 逐份阅读 `examples/runs/mock/*.md`，核对每步参数、返回、决策依据与最终结论一致。
4. 真实模型：GLM-4-Flash 两轮，第 1 轮评估中断（已修复）、第 2 轮 20/41；逐条阅读 Trace，归因写在 [03-evaluation.md](03-evaluation.md)。

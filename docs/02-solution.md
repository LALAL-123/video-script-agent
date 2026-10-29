# 02 方案

## 调用流程

```
创作需求 ──► ReActAgent.run
               │
         ┌──► 模型选择动作 + decision_note
         │     ├─ search_materials：返回素材 ID 与可用事实
         │     ├─ estimate_duration(title, shots)：每镜秒数、总时长、是否超时、script_hash
         │     ├─ check_rules(title, shots)：违规列表、script_hash
         │     └─ finish(title, shots, …) ──► guard：终稿哈希必须对上通过检查的版本
         └── 未 finish 且未超限：下一轮；超限 ──► incomplete
```

脚本由模型写在 `estimate_duration` / `check_rules` 的参数里，每改一版都要重新估算和检查；两个工具都返回 `script_hash`，把“哪一版通过了检查”变成可核对的事实。

## 动态决策点

| 观察 | 可选动作 |
|---|---|
| 缺 topic / platform / target_duration_sec | 不写脚本，`needs_input` |
| `search_materials.count = 0` | 换产品词再检索；仍无 → `no_material`，请补充素材 |
| `estimate_duration.within_target = false` | 压缩（删修饰、合并或删去非核心分镜）后重新估算；压不进 → `duration_not_met`，说明最短时长 |
| `check_rules.passed = false` | 按 violations 修改，再估算、再检查 |
| 工具失败 | 重试一次；规则检查始终失败 → `failed`，不能声称合规 |

## 规则检查（`check_rules`）

| 规则 | 检查方式 |
|---|---|
| B01 绝对化用语 | 标题与旁白不含“最强、第一、史上……” |
| B02 无出处数字 | 旁白中的每个数字/百分比必须出现在**该分镜**引用素材的事实中（型号如 X1 不算数字） |
| B03 素材 ID | 引用的 ID 必须存在 |
| B04 品牌名 | 全文至少出现一次“星拍” |
| B05 标题长度 | ≤ 30 字 |

B02 让“编造效果数据”在工具层就被发现：P01 只有“支持字幕”，写“效率提升 80%”必然违规。

## 结束护栏

`finish` 后 `guard` 计算终稿的 `script_hash`，在本轮记录中查找：

- 没有对应的估算 → `unverified`；估算超时 → `duration_not_met`；
- 没有对应的规则检查 → `unverified`（检查工具全部失败则 `failed`）；检查未通过 → `rule_not_met`；
- 引用了未检索到的素材 → `unverified`；
- `total_seconds` 与每镜秒数一律取估算结果。

模型“改了一个字却没有重新检查”就提交，也会被识别出来。

## 技术取舍

| 选择 | 理由 | 代价 |
|---|---|---|
| 脚本由模型写在工具参数里，不单设“生成脚本”工具 | 写作本身就是模型的动作；每版脚本都留在 Trace 里，可逐版对比 | Trace 较长 |
| `script_hash` 绑定检查结果 | 终稿与检查版本是否一致变成可机械核对的事实 | 任何微小改动都需重新检查 |
| 时长按字数估算 | 确定、可复现，评审能手算核对 | 与真实口播时长有偏差 |
| 数字出处按分镜检查 | 比全文检查更严格：数字必须来自该镜引用的素材 | 标题中的数字按全部引用素材检查 |
| 原生循环 + OpenAI 兼容接口 + `decision_note` + `finish` 工具 | 同题 1 | 各家 function calling 细节不同 |

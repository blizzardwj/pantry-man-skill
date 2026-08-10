# Feedback Flow — 反馈捕获、落点与复用状态机

> 反馈处理是 pantry-man skill 的运行重点。本文件是完整状态机，**任何涉及用户反馈的读写操作（捕获 / 落点 / 整理 / 消费）都以此为准**；SKILL.md 的「Feedback Capture & Reuse」章节是本文件的入口摘要。数据字段定义见 [schema.md](schema.md)。

## 术语：三层 hooks

agent 无常驻进程——反馈处理没有"后台自己找活干"的守护进程，一切整理只能**挂在宿主流程的自然执行点上**。三层 hooks 同时编码"何时触发"与"挂在哪里"：

| Hook | 触发条件 | 挂载点 | 方向 |
|------|---------|--------|------|
| `capture hook` | 对话中出现反馈信号（即时） | 对话处理流 | 写侧 · 同步 |
| `threshold hook` | 同日累积 ≥8 或同实体/同类型 ≥3 条 | 自然日界 | 写侧 · 静默批处理 |
| `review hook` | 生成采购计划/每日搭配前（仅当天有 feedback 时） | 计划生成流 | 读侧 · 兜底消费 |

写侧（capture → threshold）产出数据，读侧（review）消费数据——同一状态机首尾相接：`landing.applied: false` 的记录正是读侧消费的耗尽候选。

## ① Capture hook（写侧 · 即时捕获）

对话中出现下列信号，**立即**写一条记录到 feedback.json（不打断用户）：

| Signal | Example | type | default importance |
|--------|---------|------|--------------------|
| 纠正/替换 correction | "鲈鱼改成鲷鱼片" | preference-correction | 2 |
| 推翻画像级认知 | "根茎类都算非精制碳水" | preference-correction | 5 |
| 已有/别买 already have | "虾皮鸡蛋青椒已有" | stock-change | 3 |
| 新食材/新事实 new fact | "早餐有洋葱、自制酸奶" | ingredient-fact | 4 |
| 状态变化 state change | "苹果黄瓜吃完了" | stock-change | 3 |
| 流程建议 flow suggestion | "是否需要用 Python 验证数量？" | pairing-feedback | 5 |
| 对方案不满 dissatisfaction | 搭配被要求重做 | pairing-feedback | 3-4 |

importance anchors: 5=画像/流程级 · 4=长期习惯 · 3=状态事实 · 2=一次性微调 · 1=噪音/待观察（只日志，不沉淀）。

Record format（字段定义见 [schema.md](schema.md)）：

```json
{
  "id": "fb_x9y8z7",
  "type": "ingredient-fact | preference-correction | stock-change | pairing-feedback",
  "capturedAt": "<ISO8601+tz>",
  "source": "<user utterance summary>",
  "importance": 3,
  "content": "<structured fact / correction>",
  "landing": { "target": "pantry | shopping | profile | rule", "applied": false, "detail": "<what/where>" },
  "status": "active"
}
```

## ② Conflict avoidance（写任何落点文件前必查）

```
① 查重: does the entity already exist in the landing file?
② 同实体合并: if yes → update/merge, never duplicate (feedback records set mergedInto)
③ 以新为准: new feedback contradicts old profile/records → new wins, old marked decayed
④ 幂等: repeated content with no new info → no new record; raise original importance (+1, cap 5)
```

## ③ Landing decision（落点判定，可同时应用多个）

| 反馈类别 | 落点 | 规则 |
|---------|------|------|
| 状态事实 state fact | `pantry` / `shopping` | imp ≥ 3 applied immediately；"吃完"类写 `landing.applied: false` 作为**耗尽候选 depleted candidate**，计划时消费 |
| 约束偏好 constraint preference | `profile` | prefer / avoid / cookingStyle / notes |
| 结构偏好 structure preference | `profile.pairingTemplates` | 新增或修正模板 |
| 流程规则 flow rule | `profile.rules` | 用户级，不改 SKILL.md |

## ④ Threshold hook（写侧 · 同日静默整理）

满足任一即静默整理（同一自然日内，不打断对话）：
- 当日新反馈 importance 累积 ≥ 8
- 同实体 feedback ≥ 3 条 → merge（实体数据只更新一次，其余记录置 `mergedInto`）
- 同类型 feedback ≥ 3 条 → 检查升级：约束 → 画像偏好；结构 → pairingTemplates；流程 → profile.rules

动作：merge 同类、矛盾消解（新反馈推翻旧画像 → 旧记录置 decayed，画像以新为准）、升级沉淀（需 imp ≥ 4 或重复确认）。

## ⑤ Review hook（读侧 · 计划时兜底，仅当天有 feedback 时）

🛒采购计划或 🍽每日搭配生成时，若当天有 feedback：
1. 检索 active 且 imp ≥ 3 的反馈
2. 核对落点是否已应用；**漏落的补落**
3. **耗尽候选**：stock-change"吃完"记录（`applied: false`）→ 对应品类列为候选，标注"上次已吃完，可补"
4. **主动澄清**：上次确认闸门被删 ≥ 3 项 → 本次生成前补问一个高价值问题（仅一次，影响最大维度）

## Support rules

- **重复 = 确认信号**：同一内容第二次出现 → 原记录 importance +1（上限 5）并视为已确认
- **防噪音**：寒暄/无信息确认（"好的""谢谢"）不触发；imp = 1 只日志不沉淀

## Feedback loop (closed)

```
对话反馈 → ① Capture hook（写 feedback.json）
        → ② 冲突避免（查重 / 合并 / 以新为准 / 幂等）
        → ③ 落点判定（写入 pantry / shopping / profile）
        → ④ Threshold hook（同日阈值整理：merge / 消解 / 升级）
        → ⑤ Review hook（生成计划/搭配时：补漏落点 + 耗尽候选 + 主动澄清）
        → 生成时消费（计划遵循 profile.rules + 候选；搭配按 模板>画像>通用）
升级路径（确认后，均用户数据，不改 SKILL.md）:
  约束 constraint → profile prefer/avoid/cookingStyle/notes
  结构 structure  → profile.pairingTemplates（confirmed: true）
  流程 flow       → profile.rules
  状态 state      → pantry/shopping（applied）
```

SKILL.md 只承载通用框架——任何用户的个性化规则、模板、偏好都沉淀在用户数据中。

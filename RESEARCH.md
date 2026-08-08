# RESEARCH — 研究笔记

> 研究问题（RQ）的调研、候选方案、关键约束与决策记录。与 IDEAS.md 的状态条目互相引用。
> 状态流转同 IDEAS.md：`research` → 方案确定后落 `DECISIONS.md` → 实施后标 `implemented`。

## RQ-5：用户建议与反馈的沉淀、反思与再利用

- 状态: **planned**（2026-08-05 设计定稿，待实施；决策见 DECISIONS.md）
- 提出: 2026-08-05（见 IDEAS.md「研究问题：用户建议与反馈的沉淀、反思与再利用」）
- 动机: 用户在规划/调整中的建议和纠正是画像收敛最有价值的信号（比被动观察更直接）。2026-08-05 实况演练：用户报告真实早餐搭配（鸡肉/南瓜/青椒/黄瓜/洋葱/桃子/苹果/自制酸奶）→ 识别新食材（洋葱、自制酸奶）、酸奶来源（奶粉+益生菌）、库存状态变化（苹果黄瓜吃完）→ 画像补充 → 次日早餐按真实风格重搭。全程为即兴处理，无机制保证。
- 三问:
  1. **保存** — 反馈如何结构化沉淀？
  2. **反思** — 什么时机触发对反馈的反思/纳入？
  3. **再利用** — 沉淀后的反馈如何改进后续计划与搭配？

### 调研记录（2026-08-05，网络调研 + 领域知识）

4 类可借鉴方案：

#### ① 事实提取式沉淀（Mem0 / LangMem 路线）
- 机制: 对话后 LLM 异步提取结构化事实（用户偏好、实体状态）→ 记忆层，免配置、无侵入
- 出处: mem0.ai / github.com/mem0ai/mem0 / LangMem (LangChain)
- 已知缺陷: 过度提取噪音（Mem0 "aggressive infer"——什么都记等于什么都没记，2025-08 已有批评文章）
- 借鉴点: 提取 prompt 的写法（只提取有意义的事实）、异步处理不阻塞主流程

#### ② 记忆整合四杠杆（Hindsight 框架，2026-05 提出）
- **importance**: 什么才值得成为记忆（重要性评分门槛）
- **merge**: 同一实体的多条事实合并归一（如"苹果"的多次状态更新收敛为一条）
- **decay**: 置信度/相关性随时间衰减
- **eviction**: 淘汰机制（TTL/LRU + **salience floor**——高重要性事实不可仅因时间被淘汰）
- 出处: hindsight.vectorize.io 2026-05-21「The Consolidation Problem in Agent Memory」；已被 Mem0/Zep/Letta/LangChain 用作记忆整合的评估框架

#### ③ 反思触发机制（两条经典路线）
- **Generative Agents**（Stanford, arXiv 2304.03442）: 近期事件**重要性分总和超过阈值**才触发反思 → 反思产出高层洞察（比原始事件更抽象）存回记忆流 → 洞察与普通记忆同样参与检索；**检索评分 = recency × relevance × importance 加权**
- **Reflexion**（NeurIPS 2023, arXiv 2303.11366）: **失败信号触发**——任务被拒绝/被大量纠正 → 语言反思 → 存入 episodic memory buffer → 下次任务按反思改进
- 旁证: arXiv 2607.06765「When and How to Ask: Dynamic Preference Elicitation」— 主动澄清时机应选在**不确定性最高/信息增益最大**处（与 RQ-A 不确定性驱动澄清呼应）

#### ④ 复用/检索规则
- GA 检索评分（recency/relevance/importance 加权），反思洞察优先参与决策
- LangMem 路线: 提取的偏好写入结构化 memory block，决策时注入上下文

### 三问映射（→ pantry-man 场景）

| #5 问题 | 候选机制 | 映射到 pantry-man |
|---------|---------|-------------------|
| 保存 | ① 事实提取 / ② 四杠杆 | 定义**反馈类型**（食材事实 / 偏好纠正 / 状态变化 / 搭配反馈）+ 明确落点（库存 / 画像 / 搭配规则）；用四杠杆当整理规则（importance 分级、merge 同实体、decay/eviction 过期状态） |
| 反思 | ③ GA 阈值 / Reflexion 失败触发 | **事件驱动为主**：用户纠正或报告新事实 → 立即判断是否更新画像/数据（不打断流程）；可选计划生成后复盘 |
| 再利用 | ④ 检索评分 / 画像注入 | 反馈 → 落点（数据 / 画像偏好 / 流程规则 / 偏好模板）；搭配生成时引用 profile.pairingTemplates |

### 关键约束（不可违背）

1. **No-code 纯指令 skill** — 不能引入 Mem0/Letta/Zep 等记忆框架；只能借鉴其设计模式，落成「SKILL.md 指令 + JSON 数据结构」（AGENTS.md 硬规则 #2）
2. **跨 agent 通用**（Open Agent Skills，`[AGENT_HOME]`）— 机制不得依赖任何单一 agent 的记忆能力/框架/执行环境
3. **最小打扰原则** — 反馈收集不得变成问卷或盘点（对齐库存冷启动 UX 原则）；主动澄清只在不确定性最高处、一次一问
4. **数据落点收敛** — 反馈尽量落入既有落点（pantry/shopping 数据、profile 画像与偏好模板、SKILL.md 流程规则），不为反馈另起炉灶（除非评估证明必须）
5. **健康建议边界** — 机制产出一律为"一般性建议，非医疗建议"，免责声明不因机制而省略

### 数据结构设计（2026-08-05 三决策定稿）

**决策 1：独立 `feedback.json`**（`[AGENT_HOME]/pantry/data/feedback.json`）— profile 与 feedback 职责分离：profile 是"已收敛的画像"，feedback 是"原始反馈日志 + 沉淀轨迹"。实体数据仍落 pantry/shopping/profile（约束 4 落点收敛不变），feedback.json 只记日志与指针。
**决策 2：importance 1-5 分制**
**决策 3：保持 4 类反馈类型**，不新增 organization-feedback——存储/归置习惯归 preference-correction，在 content 中注明即可

#### 记录结构（字段定稿）

```json
{
  "id": "fb_x9y8z7",
  "type": "ingredient-fact | preference-correction | stock-change | pairing-feedback",
  "capturedAt": "2026-08-05T13:30:00+08:00",
  "source": "用户原话摘要",
  "importance": 1,
  "content": "结构化事实/纠正内容",
  "landing": { "target": "pantry|shopping|profile|rule", "applied": true, "detail": "落到哪、怎么落" },
  "status": "active | decayed | evicted",
  "mergedInto": "被合并到的记录 id（可选）"
}
```

#### 四类反馈定义

| type | 判定要点 | 典型落点 | 四杠杆 |
|------|---------|---------|--------|
| ingredient-fact | 新食材/新实体出现 | pantry（入库存）| merge 同实体细节 |
| preference-correction | 推翻/修改既有画像或做法（含存储习惯）| profile / shopping / rule | 画像级，不 decay |
| stock-change | 存量状态变化（吃完/耗竭/补货）| pantry / shopping | decay 短期事实；补货后 evict |
| pairing-feedback | 对计划/搭配的满意度或改进建议 | rule / shopping | 流程级，固化进规则 |

#### importance 锚点（1-5）

| 分值 | 含义 | 实例（2026-08-05）|
|------|------|-------------------|
| 5 | 画像级/流程级 | 根茎类=非精制碳水；数量校验需求 |
| 4 | 长期习惯 | 新鲜食材统一冷藏；常备自制酸奶+洋葱 |
| 3 | 状态事实 | 苹果/黄瓜已吃完 |
| 2 | 一次性微调 | 鲈鱼→鲷鱼片 |
| 1 | 噪音/待观察 | 暂不沉淀 |

#### 四杠杆在 feedback.json 的运作

- **merge**：同实体多条反馈 → 实体数据只更新一次，其余记录置 `mergedInto` 指针
- **decay**：stock-change 类短期事实 → 补货/新采购后置 `decayed`
- **eviction**：已 decay 且无引用价值的 → 置 `evicted`（保留日志，不删记录）
- **salience floor**：importance ≥ 4 的反馈不因时间 evict（对齐 Hindsight 框架）

### 概念消解（2026-08-05）：流程规则 / 画像偏好 / 偏好模板

早期设计使用"搭配规则"一词，与"偏好模板"重叠。按 **来源 + 生命周期** 一刀切，消解为三件套：

| 概念 | 来源 | 生命周期 | 例子 |
|------|------|---------|------|
| 流程规则 | skill 内置（通用营养知识）或流程级反馈 | 固化进 SKILL.md（需 commit）| 3-part 输出格式、素材池硬约束、QUANTITY CHECK |
| 画像偏好 | 反馈沉淀 | 长期，不 decay | prefer / avoid / cookingStyle（少油、高蛋白）|
| 偏好模板 | **只来自用户反馈** | 长期，确认后沉淀 | 早餐=蛋白+薯类+蔬果+自制酸奶 |

区分要点：规则 = 通用（任何用户都一样）；模板 = **该用户独有**（个性化搭法）；画像 = 偏好**方向**（keyword），模板 = 偏好**结构**（一餐由什么组成）。

**反馈升级路径（收拢为一条）**：

```
feedback.json（原始）→ 确认/重复 → 画像偏好 或 偏好模板（均在 profile.json）
                                ↘ 流程级问题 → SKILL.md 规则（需 commit）
```

- 反馈揭示**约束**（"太油"×3）→ 画像偏好（cookingStyle 加少油）
- 反馈揭示**结构**（"早餐固定这么吃"×2）→ 偏好模板（profile.pairingTemplates）
- 反馈揭示**流程缺口**（"数量需校验"）→ SKILL.md 流程规则（c66baab）

**偏好模板结构**（profile.json `pairingTemplates` 数组元素）：

```json
{
  "id": "pt_x9y8z7",
  "meal": "breakfast",
  "pattern": "protein + root/tuber + 2-3 veg + fruit + homemade-yogurt",
  "source": "2026-08-05 早餐报告",
  "confirmed": true
}
```

`landing.target` 保持 4 枚举：`pantry | shopping | profile | rule`——模板不新增枚举，落 `target: profile` + `detail` 注明 `pairingTemplates`。

#### 真实示例（2026-08-05 对话）

- ① ingredient-fact，imp 4："早餐有洋葱、自制酸奶"→ 入冷藏库存；酸奶"奶粉+益生菌"细节 merge 进同一实体
- ② preference-correction，imp 5："根茎类=非精制碳水"→ profile.prefer += root-vegetable-carbs，永不 decay
- ③ stock-change，imp 3："苹果黄瓜吃完"→ 黄瓜保持待购；补货后 evict
- ④ pairing-feedback，imp 5："数量需校验"→ SKILL.md QUANTITY CHECK 步骤（c66baab），固化进规则
- ⑤ preference-correction，imp 4："新鲜食材存冷藏"→ pantry 6 项移冷藏（content 注明存储习惯）
- ⑥ preference-correction，imp 2："鲈鱼改鲷鱼片"→ shopping 替换，不升级为画像规则

### 触发规则设计（2026-08-05 定稿）

三层触发模型：**即时捕获（快）→ 阈值反思（静默整理）→ 计划时回顾（兜底）**。

#### 第一层：即时捕获（事件驱动，对话中立即触发）

用户对话出现以下信号 → 立即写 feedback.json + 判断是否落点：

| 信号 | 示例 | 归类 | 默认 importance |
|------|------|------|----------------|
| 纠正/替换 | "鲈鱼改成鲷鱼片" | preference-correction | 2（一次性）|
| 推翻画像级认知 | "根茎类都算非精制碳水" | preference-correction | 5 |
| 已有/别买 | "虾皮鸡蛋青椒已有" | stock-change | 3 |
| 新食材/新事实 | "早餐有洋葱、自制酸奶" | ingredient-fact | 4 |
| 状态变化 | "苹果黄瓜吃完了" | stock-change | 3 |
| 流程建议 | "是否需要用 Python 验证数量？" | pairing-feedback | 5 |
| 对方案不满 | 搭配被要求重做 | pairing-feedback | 3-4 |

动作：imp ≥ 3 → 立即应用落点（更新库存/清单/画像）；imp ≤ 2 → 只记日志，不落点。

#### 第二层：阈值反思（GA 式静默批量整理）

触发条件（同一自然日内满足任一）：
1. 当日新反馈 **importance 累积 ≥ 8**（已确认）
2. 同实体 feedback ≥ 3 条 → 触发 merge（如"苹果"删清单→早餐出现→吃完 合成一条）
3. 同类型 feedback ≥ 3 条 → 检查是否升级为画像偏好或偏好模板（如连续 3 次"太油"→ cookingStyle 加少油；"早餐固定这么吃"×2 → pairingTemplates）

动作：merge 同类（`mergedInto` 指针）、矛盾消解（新反馈推翻旧画像 → 旧记录置 decayed，画像以新为准）、升级规则。

#### 第三层：计划时回顾（兜底）

触发：**仅当天有 feedback 时**（已确认）——🛒采购计划或 🍽每日搭配生成时作为流程内建环节：
1. 检索 active 且 imp ≥ 3 的 feedback
2. 核对是否已落入画像/库存/清单；**漏落的补落**
3. 检查是否存在该问没问的高不确定性 → 触发一次主动澄清

#### 配套规则

- **重复 = 确认信号**：同一内容第二次出现 → importance +1（上限 5）并视为已确认
- **主动澄清**：确认闸门被**删 ≥ 3 项**（已确认）算大幅修正 → 记 pairing-feedback imp 4 → **下次**计划生成时补问一个高价值问题（只在影响最大的维度，对齐最小打扰）

#### 防噪音（不触发）

- 寒暄/无信息确认（"好的""谢谢"）不触发
- 重复已有内容且无新信息 → 不新增记录，仅提升原记录 importance
- imp = 1 的待观察内容 → 只日志，不落点

### 复用规则设计（2026-08-05 定稿）

**生成时三级引用**（采购计划 / 每日搭配生成时按层级消费落点）：

```
① 模板层（最高优先）   profile.pairingTemplates —— 餐次结构定形
② 画像层              prefer/avoid/cookingStyle —— 食材选择 + 做法约束
③ 通用准则层（兜底）   SKILL.md 内置 —— 3-part 格式、素材池、营养均衡
```

- 冲突处理：模板是"结构"，**不突破健康约束**——模板要水果但画像 avoid high-sugar 且当天已超量 → 画像/健康约束优先，模板降级为参考

**落点消费表**（每个落点如何被消费）：

| 落点 | 消费方（已有机制）| 复用效果 |
|------|-----------------|---------|
| pantry | 计划库存感知 → 跳过已有 | 洋葱/酸奶入库后，计划不再推荐洋葱 |
| shopping | 避免重复 + 待购项 = 食材池 | 清单即食材池（素材→组合）|
| profile 画像偏好 | 选品 + 组合原则 | 根茎类=非精制碳水 → 薯类当主食用 |
| profile 偏好模板 | 每日搭配餐次结构（新）| 早餐按"蛋白+薯类+蔬果+酸奶"搭 |
| rule（SKILL.md）| 固化即生效（需 commit）| 数量校验每次自动跑 |

**feedback → 落点判定流程（收口）**：

```
分类 + importance（锚点表）
  → 状态事实   → pantry/shopping（数据）
  → 约束偏好   → profile（prefer/avoid/cookingStyle/notes）
  → 结构偏好   → profile.pairingTemplates（新增/修正模板）
  → 流程缺口   → rule（SKILL.md，记入 feedback 待 commit）
写入 feedback.json（landing 指针 + status=active）
```

**GA 三因子映射**：relevance（按生成任务选层——生成早餐只引用 breakfast 模板）、recency（新反馈优先于旧画像，矛盾时旧记录 decay）、importance（imp ≥ 4 必应用；imp ≤ 2 仅参考）。

**模板轮换**：同餐次积累多个模板 → confirmed 优先 + **轮换使用**，避免天天雷同。

**耗尽候选机制**（与库存感知配对）：

| 状态 | 行为 |
|------|------|
| pantry 有库存 | 跳过（已有机制）|
| 无库存、无记录 | 正常推荐 |
| 无库存 + "吃完"记录（feedback active）| 推荐 + 标注"上次已吃完，可补" |

- 载体：feedback.json 的 stock-change 记录（`landing.applied: false`）→ 第三层回顾消费 → 确认闸门决定 → 确认则写 shopping（`applied: true`）→ 购买后 pantry 补录 + feedback 置 decayed（四杠杆闭合）
- 示例："苹果吃完"→ 下次采购计划水果类候选"苹果（上次已吃完，可补）"，用户定夺

**端到端闭环示例**（2026-08-05 反馈 → 未来被消费）：

```
"早餐有洋葱酸奶"    → 库存 → 未来计划不再推洋葱
"根茎类=非精制碳水"  → 画像 → 薯类当主食选品
"早餐固定这么吃"    → 模板 → 每日搭配早餐按此结构
"数量需校验"       → 规则 → 已固化（c66baab），每次计划自动跑
"苹果吃完"        → 耗尽候选 → 下次采购可加选苹果（用户定夺）
```

### 设计状态（2026-08-05）

- 组合 **②③④ 的轻量版**：反馈打 importance 分级 → 纠正/新事实即触发反思 → 按落点复用；**避开 ① 自动全量提取**（噪音大、违背最小打扰）
- ✅ 数据结构（独立 feedback.json / importance 1-5 / 4 类反馈）— 定稿
- ✅ 触发规则（三层模型：即时捕获 / 阈值反思 / 计划时回顾）— 定稿
- ✅ 概念消解（流程规则 / 画像偏好 / 偏好模板 三件套）— 定稿
- ✅ 复用规则（三级引用 / 模板轮换 / 耗尽候选）— 定稿
- ▶ 下一步：实施（SKILL.md 指令 + schema.md + README + 数据初始化）

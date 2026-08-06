# RESEARCH — 研究笔记

> 研究问题（RQ）的调研、候选方案、关键约束与决策记录。与 IDEAS.md 的状态条目互相引用。
> 状态流转同 IDEAS.md：`research` → 方案确定后落 `DECISIONS.md` → 实施后标 `implemented`。

## RQ-5：用户建议与反馈的沉淀、反思与再利用

- 状态: **research**（待讨论定案）
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
| 再利用 | ④ 检索评分 / 画像注入 | 反馈 → 三条落点路径（数据更新 / 画像更新 / 搭配规则）；每日搭配生成时引用已确认的偏好模板 |

### 关键约束（不可违背）

1. **No-code 纯指令 skill** — 不能引入 Mem0/Letta/Zep 等记忆框架；只能借鉴其设计模式，落成「SKILL.md 指令 + JSON 数据结构」（AGENTS.md 硬规则 #2）
2. **跨 agent 通用**（Open Agent Skills，`[AGENT_HOME]`）— 机制不得依赖任何单一 agent 的记忆能力/框架/执行环境
3. **最小打扰原则** — 反馈收集不得变成问卷或盘点（对齐库存冷启动 UX 原则）；主动澄清只在不确定性最高处、一次一问
4. **数据落点收敛** — 反馈尽量落入既有三落点（profile.json 画像 / pantry+shopping 数据 / 搭配规则），不为反馈另起炉灶（除非评估证明必须）
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

#### 真实示例（2026-08-05 对话）

- ① ingredient-fact，imp 4："早餐有洋葱、自制酸奶"→ 入冷藏库存；酸奶"奶粉+益生菌"细节 merge 进同一实体
- ② preference-correction，imp 5："根茎类=非精制碳水"→ profile.prefer += root-vegetable-carbs，永不 decay
- ③ stock-change，imp 3："苹果黄瓜吃完"→ 黄瓜保持待购；补货后 evict
- ④ pairing-feedback，imp 5："数量需校验"→ SKILL.md QUANTITY CHECK 步骤（c66baab），固化进规则
- ⑤ preference-correction，imp 4："新鲜食材存冷藏"→ pantry 6 项移冷藏（content 注明存储习惯）
- ⑥ preference-correction，imp 2："鲈鱼改鲷鱼片"→ shopping 替换，不升级为画像规则

### 当前倾向（待确认）

- 组合 **②③④ 的轻量版**：反馈打 importance 分级 → 纠正/新事实即触发反思 → 按落点复用；**避开 ① 自动全量提取**（噪音大、违背最小打扰）
- 待决策项（数据结构已定稿，剩余两项）:
  1. 触发规则细则（哪些反馈事件必反思、哪些延迟到计划生成时）
  2. 复用规则（feedback → 落点的判定流程；搭配/计划生成时如何引用沉淀）

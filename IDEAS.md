# IDEAS — 问题、想法与实施追踪

> 本文件回答“为什么做、准备做什么、实施到哪一步、结果如何”，是**实施进展的唯一维护位置**。
> 研究证据与候选设计见 [RESEARCH.md](RESEARCH.md)；决策及其有效性见 [DECISIONS.md](DECISIONS.md)。
> 当前运行行为以 [SKILL.md](SKILL.md) 及其引用的 references 为准；本文件中的历史讨论不构成运行指令。

### 记录约定

- 每项使用永久编号 `IDEA-NNN` 和显式锚点 `idea-nnn`。新编号取已分配最大值加一，不复用、不因排序或标题变化而重编号。历史条目保留原标题，避免破坏旧引用。
- 状态：`idea`（尚未决定实施）→ 用户决定实施后 `planned` → 开始实施 `implementing` → 完成约定范围 `implemented`；放弃用 `dropped` 并保留原因。进入研究不等于决定实施，研究状态只在 RESEARCH 维护。
- `implemented` 不表示效果已验证。实施链接、验证结果、实际效果分开记录；有用例不等于执行通过，没有证据写“未找到执行结果／效果待观察”。
- 创建日期是问题最初提出时间；更新日期是条目维护时间。历史日期沿用原记录，不据 Git 提交时间推定讨论或批准日期。补录必须注明补录日期及来源。
- 正文按现有顺序保留、新项追加；顶部索引先列活跃事项，再列完成／放弃事项。索引只导航，不复制状态字段。
- 当前摘要可更新；详细讨论保留为历史依据，重要范围变化、采纳、放弃、替代及复核追加到“关键进展”（时间正序）。后续改进用关联条目承接，不抹掉原完成记录。细微文字修改由 Git 记录。
- 2026-09-13 为旧条目补齐编号与追溯入口；“范围／完成标准”是从已有实现或描述归纳的核对范围，不声称是当时已写下的验收条件。

### 条目模板

新想法先填编号、状态、创建日期、问题；决定实施前补范围／完成标准，完成时补实施与验证。无关联研究或决策时明确写“无”，不为小修改强建研究。

```markdown
<a id="idea-nnn"></a>
## 标题

- 编号：IDEA-NNN
- 状态：idea
- 创建：YYYY-MM-DD
- 更新：YYYY-MM-DD
- 问题与预期结果：
- 范围／完成标准：
- 关联：研究／决策／前序与后续想法（稳定链接）
- 实施：提交或 PR 链接；未提交时写“本次工作区”，提交后补链接
- 验证与效果：结果链接、覆盖范围、尚未验证部分

### 关键进展

- YYYY-MM-DD：变化、原因、证据链接
```

### 索引

活跃事项：

| 编号 | 主题 |
|------|------|
| [IDEA-003](#idea-003) | 画像收敛改进：从对话提取仍需多轮沟通 |
| [IDEA-005](#idea-005) | 研究问题：画像收敛（RQ-A / RQ-C） |
| [IDEA-013](#idea-013) | 时间戳时区格式一致性：+08:00 vs +0800 |

已完成／历史事项：

| 编号 | 主题 |
|------|------|
| [IDEA-001](#idea-001) | First-Run 初始化 |
| [IDEA-002](#idea-002) | Weekly Plan：按周采购规划 + 每日食材搭配 |
| [IDEA-004](#idea-004) | 库存冷启动 UX（Phase 2 重新定义） |
| [IDEA-006](#idea-006) | 每日搭配输出改进：食材搭配 + 最简便做法，而非菜谱 |
| [IDEA-007](#idea-007) | 库存冷启动探测：从「仅周计划」提升为通用规则 |
| [IDEA-008](#idea-008) | 规划流程重构（#1-#4）：独立功能 + 确认闸门 + 分段规划 |
| [IDEA-009](#idea-009) | 研究问题：用户建议与反馈的沉淀、反思与再利用 |
| [IDEA-010](#idea-010) | 采购计划数量校验：膳食指南基准 + 确认闸门前校验步骤 |
| [IDEA-011](#idea-011) | Feedback flow 独立成 reference 文件 |
| [IDEA-012](#idea-012) | SKILL.md 示例与输出解耦：示例锚定问题 |
| [IDEA-014](#idea-014) | 食材咨询入口 + 通用食材知识落点 |
| [IDEA-015](#idea-015) | 研究问题：用户反馈的消费语义（RQ-6） |
| [IDEA-016](#idea-016) | 采购计划参考 exemplar：正向反馈的保供（replenish）消费 |
| [IDEA-017](#idea-017) | 开发演进文档的职责、结构与追溯整理 |

<a id="idea-001"></a>
## First-Run 初始化

- 编号：IDEA-001
- 状态：implemented
- 创建：2026-07-31
- 更新：2026-09-13
- 范围／完成标准：初始化缺失的数据目录与种子文件，重复运行不覆盖已有数据。
- 关联：[DEC-001](DECISIONS.md#dec-001)
- 实施：[32c8c0f](https://github.com/blizzardwj/pantry-man-skill/commit/32c8c0f)
- 验证与效果：历史结果未独立复验，效果待观察；[证据核对](dev/documentation-review-2026-09-13.md#historical-evidence)。 相关[用例定义](dev/golden_cases/add_inventory.json)，不代表已有通过结果。

### 历史背景与讨论

- 动机: 首次使用 skill 时数据文件不存在，agent 操作会冷启动失败
- 评估: 成本低（14 行指令），解决最严重的 UX 问题；跨 agent 通用，不破坏兼容性
- 备注: 用 `[AGENT_HOME]` 保持 agent 无关；已存在时静默跳过

### 关键进展

- 2026-09-13：补录编号与追溯入口；原实施状态表述为“**implemented** (commit 32c8c0f)”。状态摘要现由本条独占维护，历史讨论不作为当前契约。

<a id="idea-002"></a>
## Weekly Plan：按周采购规划 + 每日食材搭配

- 编号：IDEA-002
- 状态：implemented
- 创建：2026-08-04
- 更新：2026-09-13
- 范围／完成标准：建立画像驱动的周规划；后续拆分由 IDEA-008 承接。
- 关联：[DEC-002](DECISIONS.md#dec-002)；后续 [IDEA-008](IDEAS.md#idea-008)
- 实施：[6d00a33](https://github.com/blizzardwj/pantry-man-skill/commit/6d00a33)
- 验证与效果：历史结果未独立复验，效果待观察；[证据核对](dev/documentation-review-2026-09-13.md#historical-evidence)。 相关[用例定义](dev/golden_cases/pool_hard_constraint.json)，不代表已有通过结果。

### 历史背景与讨论

- 动机: 真实试用后痛点——记录/查询/提醒是录入负担（购物、消耗都要手动告知 agent）。用户真正想要的是"规划产出价值"：每周采购 2 次（每次 3-4 天食材），agent 根据用户画像推荐蔬菜/水果/蛋白质/油脂/主食的品种与分量，并给出每日食材搭配（如蒸碗菜、水果沙拉碗、水煮菜+坚果碗）
- 评估: 高价值。规划功能形成闭环（画像→周规划→采购清单 shopping.json→购买记录 history→库存 pantry.json→下周规划参考剩余），复用现有数据层，不另起炉灶。分两阶段：①画像→周规划→采购清单（不依赖库存）②规划参考库存剩余联动
- 画像形态: 不搞问卷。可选 `profile.json`（饮食文化/健康状况/烹饪偏好），agent 对话中自然累积 + 首周规划后让用户确认/修正画像（二次确认优于一次问卷）
- 风险: 涉及健康建议（糖尿病/冠心病史）→ SKILL.md 必须加"非医疗建议"免责声明
- 备注: 用户示例画像：中国人、父辈有糖尿病和冠心病史、避免精制碳水、低GI碳水、少不健康油脂、加入心脑血管友好油脂、偏好蒸/煮/凉拌等极简烹饪
- 演进: 2026-08-05 真实试用后按 #1-#4 问题重构为「采购计划/每日搭配独立功能 + 周计划编排器」，见「规划流程重构」条目

### 关键进展

- 2026-09-13：补录编号与追溯入口；原实施状态表述为“**implemented**（2026-08-05 重构后由「规划流程重构」条目承接，见下）”。状态摘要现由本条独占维护，历史讨论不作为当前契约。

<a id="idea-003"></a>
## 画像收敛改进：从对话提取仍需多轮沟通

- 编号：IDEA-003
- 状态：idea
- 创建：2026-08-04
- 更新：2026-09-13
- 范围／完成标准：减少首次画像修正轮次；具体方案与验收指标尚未决定。
- 关联：[IDEA-005](IDEAS.md#idea-005)；[RQ-A](RESEARCH.md#rq-a)、[RQ-C](RESEARCH.md#rq-c)
- 实施：未实施
- 验证与效果：未实施；历史观察见下文，相关研究或修复效果尚未验证。[证据核对](dev/documentation-review-2026-09-13.md#historical-evidence)。

### 历史背景与讨论

- 动机: 首次试用中，初始画像从对话历史推断后，用户仍修正了 3 轮才收敛（纤维类型 high-fiber→soluble-fiber、烹饪时长原则、烹饪方式不炒菜加烙）。说明"从对话自然累积"虽优于问卷，但单次推断偏差仍大
- 评估: 方向是改进"首次规划前的画像引导"，例如：首轮规划前用几个高价值问题（过敏/忌口、烹饪方式、每周采购节奏）快速收敛，而非一次问卷；或规划后引导用户逐项确认
- 备注: 待将来讨论具体方案（2026-08-04 试用后记录）

### 关键进展

- 2026-09-13：补录编号与追溯入口；原实施状态表述为“**idea**（升级为研究问题，见下方条目）”。状态摘要现由本条独占维护，历史讨论不作为当前契约。

<a id="idea-004"></a>
## 库存冷启动 UX（Phase 2 重新定义）

- 编号：IDEA-004
- 状态：implemented
- 创建：2026-08-04
- 更新：2026-09-13
- 范围／完成标准：通过日常行为和轻量探测积累库存，避免首次全量盘点。
- 关联：[IDEA-007](IDEAS.md#idea-007)；[DEC-003](DECISIONS.md#dec-003)
- 实施：[70f628b](https://github.com/blizzardwj/pantry-man-skill/commit/70f628b)
- 验证与效果：历史结果未独立复验，效果待观察；[证据核对](dev/documentation-review-2026-09-13.md#historical-evidence)。

### 历史背景与讨论

- 动机: 库存感知（Phase 2）与画像冷启动同构——pantry.json 初次为空，需要用户提供。但库存比画像更难：库存是结构化事实（有什么/多少/过期），用户不可能在对话中自然流露，全量盘点 = 把"录入负担"以另一种形式请回来（原版 skill 的痛点）
- 核心设计原则: **永远不让用户"盘点"，让库存通过日常行为（购买→库存、过期提醒→消耗确认）自然形成**
- 开场策略: 不全量盘点，只问高杠杆项——长周期囤货（干货/食用油/坚果/主食），因为它们才是重复购买风险最高的；生鲜每周必买，感知与否无意义
- **UX 文案模式（去 AI 味，四个转变）**:
  1. 先认同用户身份，不直接索取数据（"像你这样注重健康饮食的人"）
  2. 共情推测代替直接提问，降低回答压力（"我觉得应该有干货和食用油囤货"）
  3. 把请求包装成服务，价值归属用户（"我来帮你记住这些"）
  4. 明示用户收益，而非 agent 逻辑（"更好地为您提供食材搭配"，不说"规划时我会避开"）
  - 示例开场: "初次接触，像你这样注重健康饮食的人，我觉得应该有干货和食用油囤货。我来帮你记住这些，更好地为您提供食材搭配。"
- 备注: 2026-08-04 讨论产出；UX 文案模式可固化为 SKILL.md 的通用对话准则（不止库存场景）

### 关键进展

- 2026-09-13：补录编号与追溯入口；原实施状态表述为“**implemented**（SKILL.md Inventory Awareness 子节 + Step 1/3 升级）”。状态摘要现由本条独占维护，历史讨论不作为当前契约。

<a id="idea-005"></a>
## 研究问题：画像收敛（RQ-A / RQ-C）

- 编号：IDEA-005
- 状态：idea
- 创建：2026-08-04
- 更新：2026-09-13
- 范围／完成标准：比较画像澄清与收敛策略；研究结论不直接代表实施批准。
- 关联：[IDEA-003](IDEAS.md#idea-003)；[RQ-A](RESEARCH.md#rq-a)、[RQ-C](RESEARCH.md#rq-c)
- 实施：未实施
- 验证与效果：未实施；历史观察见下文，相关研究或修复效果尚未验证。[证据核对](dev/documentation-review-2026-09-13.md#historical-evidence)。

### 历史背景与讨论

- 背景：由“画像收敛改进”提升而来，关注最小用户打扰与画像保真度的张力。
- 历史研究内容：问题、假设与评测方案已迁入 [RQ-A](RESEARCH.md#rq-a) 与 [RQ-C](RESEARCH.md#rq-c)；原文可由 [9457803](https://github.com/blizzardwj/pantry-man-skill/commit/9457803) 追溯。

### 关键进展

- 2026-09-13：原状态 `research` 迁到研究条目表达；实施状态归为 `idea`，未据“开展研究”推定已批准实施。原假设迁入 [RQ-A](RESEARCH.md#rq-a)、[RQ-C](RESEARCH.md#rq-c)。

<a id="idea-006"></a>
## 每日搭配输出改进：食材搭配 + 最简便做法，而非菜谱

- 编号：IDEA-006
- 状态：implemented
- 创建：2026-08-04
- 更新：2026-09-13
- 范围／完成标准：每日搭配输出食材、价值、简便做法；后续做法原则见 DEC-010。
- 关联：[DEC-010](DECISIONS.md#dec-010)；[IDEA-012](IDEAS.md#idea-012)
- 实施：[2194b19](https://github.com/blizzardwj/pantry-man-skill/commit/2194b19)、[2143bf0](https://github.com/blizzardwj/pantry-man-skill/commit/2143bf0)
- 验证与效果：历史结果未独立复验，效果待观察；[证据核对](dev/documentation-review-2026-09-13.md#historical-evidence)。 相关[用例定义](dev/golden_cases/pairing_minimal_methods.json)，不代表已有通过结果。

### 历史背景与讨论

- 动机: 试用中发现"蒸碗菜/水果沙拉碗/水煮菜+坚果碗"这种菜谱式输出对用户参考价值有限——用户要的是"食材怎么合理搭配"，以及"最简便且健康的做法"，而不是菜名
- 评估: 改动小（SKILL.md Step 4 指令重写），提升直接——输出从"菜名"变为"食材组合+1-2句做法"，更贴近实际决策
- 备注: 2026-08-04 实施。最终形态为固定 3-part pattern：①食材组合 ②价值 ③最简便做法（示例：鸡胸肉+香菇+西兰花（高蛋白+水溶性纤维+护肝）→ 鸡胸肉烙片，香菇西兰花焯水2分钟拌橄榄油）

### 关键进展

- 2026-09-13：补录编号与追溯入口；原实施状态表述为“**implemented** (commit 2194b19)”。状态摘要现由本条独占维护，历史讨论不作为当前契约。

<a id="idea-007"></a>
## 库存冷启动探测：从「仅周计划」提升为通用规则

- 编号：IDEA-007
- 状态：implemented
- 创建：2026-08-05
- 更新：2026-09-13
- 范围／完成标准：任意库存读取可触发一次冷启动探测，用户应答后才设置标记。
- 关联：[DEC-003](DECISIONS.md#dec-003)；前序 [IDEA-004](IDEAS.md#idea-004)
- 实施：[0ad1af2](https://github.com/blizzardwj/pantry-man-skill/commit/0ad1af2)
- 验证与效果：历史结果未独立复验，效果待观察；[证据核对](dev/documentation-review-2026-09-13.md#historical-evidence)。

### 历史背景与讨论

- 动机: 试用发现——long-cycle 探测只接入 Weekly Plan Step 1，用户查看空库存时不会触发；而「查看库存」恰恰是收集长周期囤货信息的最佳时机（用户正关注库存状态，回答意愿最高）。实测佐证：08-04 周计划生成了 24 项购物清单，但 pantry.json 仍为空——该信息从未被收集到
- 评估: 改动小（Cold-start 子节重写 + View by zone 加探测步骤 + meta 标记），探测时机从单一触发点扩展为「任意库存读取」；`meta.longCycleProbed` 保证每个数据文件只探测一次（缺失视为 false，向后兼容已有数据）
- 备注: 2026-08-05 试用后记录；标记语义——用户应答（确认有/说没有）即置 true，不应答则不置，留待下次自然触点

### 关键进展

- 2026-09-13：补录编号与追溯入口；原实施状态表述为“**implemented** (commit 0ad1af2)”。状态摘要现由本条独占维护，历史讨论不作为当前契约。

<a id="idea-008"></a>
## 规划流程重构（#1-#4）：独立功能 + 确认闸门 + 分段规划

- 编号：IDEA-008
- 状态：implemented
- 创建：2026-08-05
- 更新：2026-09-13
- 范围／完成标准：采购计划、每日搭配独立，周计划按段编排并经确认闸门写入。
- 关联：[DEC-004](DECISIONS.md#dec-004)；前序 [IDEA-002](IDEAS.md#idea-002)
- 实施：[aaf3813](https://github.com/blizzardwj/pantry-man-skill/commit/aaf3813)
- 验证与效果：历史结果未独立复验，效果待观察；[证据核对](dev/documentation-review-2026-09-13.md#historical-evidence)。 相关[用例定义](dev/golden_cases/pool_hard_constraint.json)，不代表已有通过结果。

### 历史背景与讨论

- 动机: 试用 Weekly Plan 后开发者提出的 4 个问题：①清单与搭配的顺序/依赖不清（搭配应派生自清单，素材→组合）②一次输出整周清单+7天搭配信息量过大、3-4天采购对应整周搭配错位、清单写入前无确认机会 ③搭配同样需要用户参与且显示不友好（早/午/晚应列表化）④采购计划与每日搭配应拆为独立功能，周计划降为编排器
- 评估: 重构为三个模块——🛒采购计划（确认闸门：展示→确认→写入）、🍽每日搭配（食材池=已确认清单∪库存，按天分块列表显示，支持局部调整与清单联动重生成）、📆周计划（编排器：按 shoppingRhythm 切段，逐段调用前两者并逐段确认）；schema 无需变更（确认后写入即已确认，unchecked 即当前段落待购项）
- 备注: 配套决策见 DECISIONS.md [2026-08-05]；第 5 项问题（用户反馈沉淀）留作研究条目

### 关键进展

- 2026-09-13：补录编号与追溯入口；原实施状态表述为“**implemented**（commit aaf3813）”。状态摘要现由本条独占维护，历史讨论不作为当前契约。

<a id="idea-009"></a>
## 研究问题：用户建议与反馈的沉淀、反思与再利用

- 编号：IDEA-009
- 状态：implemented
- 创建：2026-08-05
- 更新：2026-09-13
- 范围／完成标准：反馈捕获、整理与复用接入数据及计划流程；此次不修复已发现的语义缺口。
- 关联：[RQ-5](RESEARCH.md#rq-5)；[DEC-007](DECISIONS.md#dec-007)；后续 [IDEA-011](IDEAS.md#idea-011)、[IDEA-015](IDEAS.md#idea-015)
- 实施：[ba3c75b](https://github.com/blizzardwj/pantry-man-skill/commit/ba3c75b)、[9f3ead5](https://github.com/blizzardwj/pantry-man-skill/commit/9f3ead5)、[2b91c88](https://github.com/blizzardwj/pantry-man-skill/commit/2b91c88)、[76b6399](https://github.com/blizzardwj/pantry-man-skill/commit/76b6399)、[d27171b](https://github.com/blizzardwj/pantry-man-skill/commit/d27171b)、[7cb0318](https://github.com/blizzardwj/pantry-man-skill/commit/7cb0318)、[6b20ccc](https://github.com/blizzardwj/pantry-man-skill/commit/6b20ccc)、[e8b81bb](https://github.com/blizzardwj/pantry-man-skill/commit/e8b81bb)、[6e6da4d](https://github.com/blizzardwj/pantry-man-skill/commit/6e6da4d)
- 验证与效果：历史结果未独立复验，效果待观察；[证据核对](dev/documentation-review-2026-09-13.md#historical-evidence)。 相关[用例定义](dev/golden_cases/stock_change_deplete.json)，不代表已有通过结果。

### 历史背景与讨论

- 背景: 开发者流程分析第 5 项——用户在规划/调整中的建议和纠正是画像收敛最有价值的信号（比被动观察更直接），如何设计一套机制：保存（如何结构化记录？）、反思（何时/如何纳入画像与推荐规则？）、再利用（如何改进后续计划与搭配？）。与 RQ-A/RQ-C 画像收敛研究同源
- 备注: 完整调研与设计见 [RESEARCH.md](RESEARCH.md)；配套决策见 DECISIONS.md [2026-08-05] RQ-5 反馈机制设计；实施 = SKILL.md Feedback Capture & Reuse 章节（捕获/三层触发/闭环）+ schema.md（feedback.json + pairingTemplates + rules）

### 关键进展

- 2026-09-13：补录编号与追溯入口；原实施状态表述为“**implemented**（2026-08-05 设计并实施，commit 2b91c88..6e6da4d）”。状态摘要现由本条独占维护，历史讨论不作为当前契约。 本次审查发现的 feedback/reuse 问题集中登记于 [RQ-5](RESEARCH.md#rq-5) 的当前局限，后续另行修复。

<a id="idea-010"></a>
## 采购计划数量校验：膳食指南基准 + 确认闸门前校验步骤

- 编号：IDEA-010
- 状态：implemented
- 创建：2026-08-05
- 更新：2026-09-13
- 范围／完成标准：确认闸门前按人数和天数核对建议采购量，提供软提示。
- 关联：[DEC-005](DECISIONS.md#dec-005)
- 实施：[c66baab](https://github.com/blizzardwj/pantry-man-skill/commit/c66baab)
- 验证与效果：历史结果未独立复验，效果待观察；[证据核对](dev/documentation-review-2026-09-13.md#historical-evidence)。

### 历史背景与讨论

- 动机: 真实试用复算对照《中国居民膳食指南》发现——计划分量无基准，agent 凭直觉给量，清单总量超单人 3-4 天需求 1.5-2 倍（蔬菜 914g/天 vs 300-500、水果 777g/天 vs 200-350、肉鱼 314g/天 vs 120-200、薯类缺失）；确认闸门只查品种不查数量，超配未被拦截
- 评估: 校验必须内建且置于确认闸门之前。采用纯指令式——基准表放 references/quantity_benchmark.md（成人每日参考量/单件克重/品类归属/容差规则），agent 读表做简单算术（每日区间 × 段天数 × 人数）；不引入脚本，符合 AGENTS.md「No code, no scripts」与跨 agent 原则——开发期 Python 仅用于定位问题，其产出沉淀为基准表
- 备注: 配套决策见 DECISIONS.md [2026-08-05] 数量校验；profile.json 新增 household.persons（默认 1）；生鲜从严、耐放从宽、只软提示不硬拦

### 关键进展

- 2026-09-13：补录编号与追溯入口；原实施状态表述为“**implemented** (commit c66baab)”。状态摘要现由本条独占维护，历史讨论不作为当前契约。

<a id="idea-011"></a>
## Feedback flow 独立成 reference 文件

- 编号：IDEA-011
- 状态：implemented
- 创建：2026-08-09
- 更新：2026-09-13
- 范围／完成标准：提取 feedback flow，并在反馈处理和计划生成入口建立引用。
- 关联：[RQ-5](RESEARCH.md#rq-5)；[DEC-008](DECISIONS.md#dec-008)、[DEC-009](DECISIONS.md#dec-009)；前序 [IDEA-009](IDEAS.md#idea-009)
- 实施：[60e34ae](https://github.com/blizzardwj/pantry-man-skill/commit/60e34ae)
- 验证与效果：历史结果未独立复验，效果待观察；[证据核对](dev/documentation-review-2026-09-13.md#historical-evidence)。 相关[用例定义](dev/golden_cases/landing_onion_yogurt.json)，不代表已有通过结果。

### 历史背景与讨论

- 动机: feedback flow（Capture → Conflict avoidance → Landing decision → 三层触发 → 闭环）是 agent + skill 运行的重点，目前以散文形式嵌在 SKILL.md 正文。风险：①SKILL.md 正文越长，agent 一次载入成本越高、关键流程被浏览略过的概率越大，可靠性下降；②feedback 流程与库存/购物等常规操作性质不同——它是跨章节的状态机，理应独立
- 评估: 成本低（从 SKILL.md 移出流程文本到 `references/feedback_flow.md`，正文保留一行 citation 链接）；收益——SKILL.md 瘦身、流程可独立维护与演进、与 `references/quantity_benchmark.md` 的既有模式同构；风险——agent 必须按 citation 主动加载 reference 才能执行流程，citation 要写得明确（如"生成搭配/计划前必读"）
- 备注: 2026-08-09 真实试用暴露早餐雷同问题后讨论产出；实施时同步检查 schema.md 中 landing 定义是否随迁或互链
- 触发点模型（2026-08-09 确认）: flow 双向触发——①写侧：对话中反馈信号出现即读 flow（Capture→Conflict avoidance→Landing decision→写 feedback.json+落点文件），不经计划生成；②读侧：采购计划/每日搭配生成前读 flow（Layer 3 plan-time review：检索 active 反馈、补漏落点、耗尽候选补清单、删改≥3项时澄清）。①②同一状态机首尾，`landing.applied:false` 的记录即读侧消费的耗尽候选。因此 citation 至少出现在 SKILL.md 两处：反馈捕获章节 + 计划生成步骤
- 迁移边界（2026-08-09 确认）: Reflection triggers（三层 + Support rules）**必须整体迁入** feedback_flow.md——Layer 1=Capture、Layer 2=同日静默整理（merge/消解/升级）、Layer 3=读侧消费，三层跨写读两侧，拆出则状态机残缺。SKILL.md 反馈章节仅留概述 + 原则声明（用户数据 vs SKILL.md 分工）+ 双处 citation；schema.md 数据结构定义不动，与 flow 互链
- 术语（2026-08-09 确认）: 统一为**三层 hooks**——capture hook / threshold hook / review hook（agent 无常驻进程，整理只能挂在宿主流程自然执行点上，hooks 同时编码"何时触发"与"挂在哪里"）；见 DECISIONS.md [2026-08-09]

### 关键进展

- 2026-09-13：补录编号与追溯入口；原实施状态表述为“**implemented** (commit 60e34ae)”。状态摘要现由本条独占维护，历史讨论不作为当前契约。 本次审查发现的 feedback/reuse 问题集中登记于 [RQ-5](RESEARCH.md#rq-5) 的当前局限，后续另行修复。

<a id="idea-012"></a>
## SKILL.md 示例与输出解耦：示例锚定问题

- 编号：IDEA-012
- 状态：implemented
- 创建：2026-08-09
- 更新：2026-09-13
- 范围／完成标准：搭配输出示例用类别占位符表达格式，减少具体食材锚定。
- 关联：[IDEA-006](IDEAS.md#idea-006)；无独立决策条目（历史方案选择见下文）
- 实施：[e47b3c8](https://github.com/blizzardwj/pantry-man-skill/commit/e47b3c8)
- 验证与效果：历史结果未独立复验，效果待观察；[证据核对](dev/documentation-review-2026-09-13.md#historical-evidence)。 相关[用例定义](dev/golden_cases/dry_good_no_soup.json)，不代表已有通过结果。

### 历史背景与讨论

- 动机: 真实试用发现——每日搭配推荐大量复用 SKILL.md 示例的具体食材与做法措辞（"鸡胸肉平底锅少油烙片""焯水N分钟拌油"一字不差复现）。LLM 把示例当模板库，内容锚定远强于格式学习；示例本意是格式示范，却同时锚定了输出内容，导致搭配趋同（叠加早餐雷同问题）
- 评估: 根因是示例同时传递「格式」与「内容」两个信号，未显式解耦。方案 A（示例去食材化，类别占位符保留格式骨架）= 最小改动，当前采用；方案 B（保留示例 + 显式反锚定声明）；方案 C（示例降级 references/pairing_examples.md，2-3 个不同风格示例，SKILL.md 只留 workflow + general guide + citation，与 feedback_flow/quantity_benchmark 架构一致）= 未来演进方向
- 备注: 采购计划类别表（蔬菜/蛋白质/油脂枚举）性质为「内容推荐」而非「格式示例」，锚定风险低（枚举非组合示例），本次不动；若未来推荐出现趋同再评估

### 关键进展

- 2026-09-13：补录编号与追溯入口；原实施状态表述为“**implemented**（2026-08-09 方式 A 示例去食材化，commit e47b3c8）”。状态摘要现由本条独占维护，历史讨论不作为当前契约。

<a id="idea-013"></a>
## 时间戳时区格式一致性：+08:00 vs +0800

- 编号：IDEA-013
- 状态：idea
- 创建：2026-08-13
- 更新：2026-09-13
- 范围／完成标准：明确时间戳时区格式或增加验证；尚未选择处理方案。
- 关联：无独立研究或决策；关联 [开发验证](dev/README.md)
- 实施：未实施
- 验证与效果：未实施；历史观察见下文，相关研究或修复效果尚未验证。[证据核对](dev/documentation-review-2026-09-13.md#historical-evidence)。

### 历史背景与讨论

- 动机: L2 黄金用例 add_inventory 首次端到端跑通时，真实 agent 把 meta.lastUpdated 写成 2026-08-13T11:23:01+0800（无冒号），而 SKILL.md Timestamp Format 与 schema.md 示例均为 +08:00（带冒号）。两者都合法 ISO 8601，但暴露「指令说 +08:00、agent 写 +0800」的 gap
- 评估: 轻微、不影响功能（dates 用 YYYY-MM-DD 是对的）。处理选项：①SKILL.md 明确要求带冒号（收紧）②schema 放宽接受两种（兼容）③断言引擎加时间戳/日期格式校验（增强 golden case，通用价值高）④不管（太轻微）。倾向 ③ 顺带做——把「时间戳/日期格式校验」作为断言引擎的通用谓词，可复用到所有涉及 bought/expires/capturedAt 的用例
- 备注: 由 dev/run_golden.py + delegate_task 端到端首跑暴露；是 golden case 价值的第一个实证（测出指令 vs 执行的细微落差，而非仅 PASS/FAIL）

### 关键进展

- 2026-09-13：补录编号与追溯入口；原实施状态表述为“idea”。状态摘要现由本条独占维护，历史讨论不作为当前契约。

<a id="idea-014"></a>
## 食材咨询入口 + 通用食材知识落点

- 编号：IDEA-014
- 状态：implemented
- 创建：2026-08-15
- 更新：2026-09-13
- 范围／完成标准：新增独立食材咨询及通用知识引用，复用用户画像。
- 关联：[DEC-012](DECISIONS.md#dec-012)
- 实施：[f8e9455](https://github.com/blizzardwj/pantry-man-skill/commit/f8e9455)、[b1557d4](https://github.com/blizzardwj/pantry-man-skill/commit/b1557d4)
- 验证与效果：旧 DEC-012 记载 static validation PASS，但未找到该次执行报告；效果待观察。[证据核对](dev/documentation-review-2026-09-13.md#historical-evidence)。

### 历史背景与讨论

- 动机: 用户问「海带/木耳/银耳/魔芋这类水溶性膳食纤维食物怎么搭」，答案是「通用知识 × 个性化需求」的两层结合体——通用层（无味高纤维食材怎么提味、有什么安全建议）谁问都一样；个性化层（控糖护肝控LDL、凉拌/煮/蒸/烙、常备洋葱酸奶）是"我"独有。现有两个入口都不覆盖：🛒采购计划答"买什么"、🍽每日搭配答"今天吃什么"，缺一个"用户点名某类食材问怎么吃"的咨询入口；且通用食材知识（提味原理、安全建议）目前只活在 agent 脑内，无落点。
- 评估: 范围小。个性化层 100% 复用现有 profile.json（prefer/avoid/cookingStyle/常备食材），无需新收集、不改 schema；唯一缺口是通用食材知识无落点。做法 = 在已有「通用准则层 × 画像层」结合方式上加第三个入口（食材咨询）+ 补一个通用知识落点（references/ 食材知识文件），不新起机制。关键边界：只补「安全建议 + 类别级提味原理」，不写「典型搭法/固定食谱」——那是每日搭配生成器的活，写死会与库存/画像冲突且僵化。
- 备注: 2026-08-15 讨论产出。核心洞察：不是"食材搭配"缺功能，是"通用食材知识"缺个家；问题可泛化到任何食材类（根茎/绿叶/豆类/菌菇…），水溶性纤维只是第一例。知识文件三件套 = 特性（客观事实）/ 提味原理（通用方法）/ 安全建议（基于客观事实的可执行饮食建议——如"木耳冷藏泡、现泡现吃"，而非单纯罗列事实）。

### 关键进展

- 2026-09-13：补录编号与追溯入口；原实施状态表述为“**implemented**（commit f8e9455 + b1557d4）”。状态摘要现由本条独占维护，历史讨论不作为当前契约。

<a id="idea-015"></a>
## 研究问题：用户反馈的消费语义（RQ-6）

- 编号：IDEA-015
- 状态：implemented
- 创建：2026-09-08
- 更新：2026-09-13
- 范围／完成标准：实例范例落点、复用、结构泛化及升模板门槛；采购保供另见 IDEA-016。
- 关联：[RQ-6](RESEARCH.md#rq-6)；[DEC-013](DECISIONS.md#dec-013)；前序 [IDEA-009](IDEAS.md#idea-009)；后续 [IDEA-016](IDEAS.md#idea-016)
- 实施：[42ab337](https://github.com/blizzardwj/pantry-man-skill/commit/42ab337)、[497a8cc](https://github.com/blizzardwj/pantry-man-skill/commit/497a8cc)、[78e9b02](https://github.com/blizzardwj/pantry-man-skill/commit/78e9b02)、[0097dd8](https://github.com/blizzardwj/pantry-man-skill/commit/0097dd8)、[3990f6c](https://github.com/blizzardwj/pantry-man-skill/commit/3990f6c)、[caa9325](https://github.com/blizzardwj/pantry-man-skill/commit/caa9325)
- 验证与效果：历史结果未独立复验，效果待观察；[证据核对](dev/documentation-review-2026-09-13.md#historical-evidence)。

### 历史背景与讨论

- 动机: 用户自创一道菜想保存复用，本质不是"找个落点"，而是"用户反馈如何被消费"。RQ-5 已解决「保存+再利用」，但「消费」有一个粒度空档——现有落点消费表覆盖画像级/结构级/规则级，独缺「实例级」（一个具体验证过的菜品/范例）的消费路径。消费语义不清 → 持久化无从谈起（消费方式决定存储形态）。
- 评估: 已从「具体菜谱落点」升维为「反馈消费语义」研究。完整调研（推荐系统显式/隐式/半显式反馈、消费粒度画像级/交互级/实例级/结构级、在线 bandit/RL、负反馈响应性）见 RESEARCH.md RQ-6。
- 备注: 2026-09-08 对话产出；原以「用户自创菜谱的存储与复用」记入（d3963a3），后经用户澄清本质上抽象为「反馈如何被消费」，升维为研究问题 RQ-6。全链路已实施：exemplar 落点 + 每日搭配复用/结构泛化 + 采购计划保供 + 范例→模板上升路径（experimental 方案见 RESEARCH.md RQ-6）。

### 关键进展

- 2026-09-13：补录编号与追溯入口；原实施状态表述为“**implemented**（实例级 exemplar 消费全链路 + 范例→模板上升路径，见 DECISIONS.md [2026-09-08]）”。状态摘要现由本条独占维护，历史讨论不作为当前契约。 原 RESEARCH 的“上升路径待实施”属于过期进展；按 [5963368](https://github.com/blizzardwj/pantry-man-skill/commit/5963368) 与上述实现提交核对，保留 implemented，实验效果仍待验证。

<a id="idea-016"></a>
## 采购计划参考 exemplar：正向反馈的保供（replenish）消费

- 编号：IDEA-016
- 状态：implemented
- 创建：2026-09-08
- 更新：2026-09-13
- 范围／完成标准：采购计划检查范例缺失主料并提出建议，数量与确认闸门继续适用。
- 关联：[RQ-6](RESEARCH.md#rq-6)；[DEC-014](DECISIONS.md#dec-014)；前序 [IDEA-015](IDEAS.md#idea-015)
- 实施：[861d1c2](https://github.com/blizzardwj/pantry-man-skill/commit/861d1c2)
- 验证与效果：历史结果未独立复验，效果待观察；[证据核对](dev/documentation-review-2026-09-13.md#historical-evidence)。

### 历史背景与讨论

- 动机: exemplar（用户验证过的拿手菜）的正向反馈应**双向消费**——每日搭配「复用」（料齐了照做）+ 采购计划「保供」（主料持续可得）。只做复用会断环：主料一吃完（如鲷鱼），范例就被"冻死"，永远触发不了。正向反馈的本质是"我想继续吃它"，对应推荐系统里点赞/收藏同时提升**复用权重**与**复购/补货倾向**。
- 评估: 与 RQ-5 已有「耗尽候选」（负向吃完→补货）拼成采购计划"反馈驱动补货"的两翼。**简化规则（2026-09-08 用户拍板）**：生成采购计划读 `profile.exemplars`，凡范例主料**在库存中没有** → 纳入采购建议并标注「你的拿手菜 X 需要它」；库存已有 → 跳过（stock-aware 已覆盖）。**不区分保存周期**——周期长短不是主要因素，库存缺不缺才是唯一判据。数量与去重仍由 quantity benchmark + 确认闸门兜底。
- 备注: 2026-09-08 对话产出；属 RQ-6「用户反馈的消费语义」的**第二消费出口**（第一出口 = 每日搭配复用）。已实施（SKILL.md 采购计划 5b 步骤，commit 861d1c2）；决策见 DECISIONS.md [2026-09-08]。

### 关键进展

- 2026-09-13：补录编号与追溯入口；原实施状态表述为“**implemented**（commit 861d1c2，SKILL.md 采购计划 5b 步骤）”。状态摘要现由本条独占维护，历史讨论不作为当前契约。

<a id="idea-017"></a>
## 开发演进文档的职责、结构与追溯整理

- 编号：IDEA-017
- 状态：implemented
- 创建：2026-09-13
- 更新：2026-09-13
- 问题与预期结果：想法、研究、决策重复维护进展，历史草案容易被当作当前规范；需要能追溯问题、选择、实现与验证。
- 范围／完成标准：三文档明确边界；现有条目具有稳定编号与链接；状态分工明确；历史转折保留；已完成事项关联实现与验证证据或明确缺口；同步 AGENTS 维护规则。
- 关联：[DEC-016](DECISIONS.md#dec-016)；本项直接依据用户确认实施，无独立研究条目。
- 实施：本次工作区中的 IDEAS.md、RESEARCH.md、DECISIONS.md、AGENTS.md 和开发期验证报告；尚未提交，提交时补提交链接。
- 验证与效果：[本次验证](dev/documentation-review-2026-09-13.md#documentation-checks)；文档检查不代表反馈业务验证，长期维护效果待观察。

### 关键进展

- 2026-09-13：用户确认先完成四项文档治理，再处理 feedback/reuse；按此范围完成文档整理，保留原始设计供下一步复核。

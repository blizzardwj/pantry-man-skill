# IDEAS — 问题、想法与实施追踪

> 本文件回答“为什么做、准备做什么、实施到哪一步、结果如何”，是**实施进展的唯一维护位置**。
> 研究证据与候选设计见 [RESEARCH.md](RESEARCH.md)；决策及其有效性见 [DECISIONS.md](DECISIONS.md)。
> 当前运行行为以 [SKILL.md](../SKILL.md) 及其引用的 references 为准；本文件中的历史讨论不构成运行指令。

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
| [IDEA-023](#idea-023) | 修复、价值提升与扩大使用待办清单 |

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
| [IDEA-018](#idea-018) | 反馈事实落点与耗尽候选生命周期分离 |
| [IDEA-019](#idea-019) | 语音输入条件下的范围收敛与核心流程改进 |
| [IDEA-020](#idea-020) | 用户输入进入反馈的边界：业务操作与可复用反馈分离 |
| [IDEA-021](#idea-021) | 日常购买报告默认完成对应购物项 |
| [IDEA-022](#idea-022) | 开发演进记录移入 dev/：与 skill 运行文件分开 |
| [IDEA-024](#idea-024) | 每日搭配食材池按用餐时点区分（待办 F-01） |
| [IDEA-025](#idea-025) | 过期条目保留并询问处置（待办 F-02） |
| [IDEA-026](#idea-026) | 定时提醒宿主无关化（待办 F-03） |
| [IDEA-027](#idea-027) | 运行文档内矛盾清理（待办 F-04） |
| [IDEA-028](#idea-028) | 首次写入前才初始化、收窄触发描述（待办 F-05） |
| [IDEA-029](#idea-029) | 库存过期状态读取时计算（待办 F-06） |
| [IDEA-030](#idea-030) | 采购提案记录时段与来源计划（待办 F-07） |
| [IDEA-031](#idea-031) | 按奥卡姆剃刀与 YAGNI 收敛运行契约（待办 V-01、V-02） |
| [IDEA-032](#idea-032) | 首次 agent 执行暴露的问题修复：名称保留原话、用例断言修正 |
| [IDEA-033](#idea-033) | 照片输入：小票直接记录、识别类照片先确认（待办 A-04 扩展） |
| [IDEA-034](#idea-034) | 回复跟随用户语言，支持英文用户（待办 V-05） |
| [IDEA-035](#idea-035) | 补齐测试覆盖缺口，修订画像创建与月度统计规则 |

<a id="idea-001"></a>
## First-Run 初始化

- 编号：IDEA-001
- 状态：implemented
- 创建：2026-07-31
- 更新：2026-10-11
- 范围／完成标准：初始化缺失的数据目录与种子文件，重复运行不覆盖已有数据。
- 关联：[DEC-001](DECISIONS.md#dec-001)
- 实施：[32c8c0f](https://github.com/blizzardwj/pantry-man-skill/commit/32c8c0f)
- 验证与效果：历史结果未独立复验，效果待观察；[证据核对](documentation-review-2026-09-13.md#historical-evidence)。 相关[用例定义](golden_cases/add_inventory.json)，不代表已有通过结果。

### 历史背景与讨论

- 动机: 首次使用 skill 时数据文件不存在，agent 操作会冷启动失败
- 评估: 成本低（14 行指令），解决最严重的 UX 问题；跨 agent 通用，不破坏兼容性
- 备注: 用 `[AGENT_HOME]` 保持 agent 无关；已存在时静默跳过

### 关键进展

- 2026-09-13：补录编号与追溯入口；原实施状态表述为“**implemented** (commit 32c8c0f)”。状态摘要现由本条独占维护，历史讨论不作为当前契约。
- 2026-10-11：初始化时机由 [IDEA-028](#idea-028) 改为“首次写入前”（[DEC-026](DECISIONS.md#dec-026)）；本条原完成记录保留。

<a id="idea-002"></a>
## Weekly Plan：按周采购规划 + 每日食材搭配

- 编号：IDEA-002
- 状态：implemented
- 创建：2026-08-04
- 更新：2026-10-11
- 范围／完成标准：建立画像驱动的周规划；后续拆分由 IDEA-008 承接。
- 关联：[DEC-002](DECISIONS.md#dec-002)；后续 [IDEA-008](IDEAS.md#idea-008)
- 实施：[6d00a33](https://github.com/blizzardwj/pantry-man-skill/commit/6d00a33)
- 验证与效果：历史结果未独立复验，效果待观察；[证据核对](documentation-review-2026-09-13.md#historical-evidence)。 相关[用例定义](golden_cases/pool_hard_constraint.json)，不代表已有通过结果。

### 历史背景与讨论

- 动机: 真实试用后痛点——记录/查询/提醒是录入负担（购物、消耗都要手动告知 agent）。用户真正想要的是"规划产出价值"：每周采购 2 次（每次 3-4 天食材），agent 根据用户画像推荐蔬菜/水果/蛋白质/油脂/主食的品种与分量，并给出每日食材搭配（如蒸碗菜、水果沙拉碗、水煮菜+坚果碗）
- 评估: 高价值。规划功能形成闭环（画像→周规划→采购清单 shopping.json→购买记录 history→库存 pantry.json→下周规划参考剩余），复用现有数据层，不另起炉灶。分两阶段：①画像→周规划→采购清单（不依赖库存）②规划参考库存剩余联动
- 画像形态: 不搞问卷。可选 `profile.json`（饮食文化/健康状况/烹饪偏好），agent 对话中自然累积 + 首周规划后让用户确认/修正画像（二次确认优于一次问卷）
- 风险: 涉及健康建议（糖尿病/冠心病史）→ SKILL.md 必须加"非医疗建议"免责声明
- 备注: 用户示例画像：中国人、父辈有糖尿病和冠心病史、避免精制碳水、低GI碳水、少不健康油脂、加入心脑血管友好油脂、偏好蒸/煮/凉拌等极简烹饪
- 演进: 2026-08-05 真实试用后按 #1-#4 问题重构为「采购计划/每日搭配独立功能 + 周计划编排器」，见「规划流程重构」条目

### 关键进展

- 2026-09-13：补录编号与追溯入口；原实施状态表述为“**implemented**（2026-08-05 重构后由「规划流程重构」条目承接，见下）”。状态摘要现由本条独占维护，历史讨论不作为当前契约。
- 2026-10-11：周计划不再是独立编排功能，“这周买什么”即下一趟采购计划（[IDEA-031](#idea-031)、[DEC-029](DECISIONS.md#dec-029)）；本条原完成记录保留。

<a id="idea-003"></a>
## 画像收敛改进：从对话提取仍需多轮沟通

- 编号：IDEA-003
- 状态：idea
- 创建：2026-08-04
- 更新：2026-10-12
- 范围／完成标准：减少首次画像修正轮次；具体方案与验收指标尚未决定。
- 关联：[IDEA-005](IDEAS.md#idea-005)；[RQ-A](RESEARCH.md#rq-a)、[RQ-C](RESEARCH.md#rq-c)
- 实施：未实施
- 验证与效果：未实施；历史观察见下文，相关研究或修复效果尚未验证。[证据核对](documentation-review-2026-09-13.md#historical-evidence)。

### 历史背景与讨论

- 动机: 首次试用中，初始画像从对话历史推断后，用户仍修正了 3 轮才收敛（纤维类型 high-fiber→soluble-fiber、烹饪时长原则、烹饪方式不炒菜加烙）。说明"从对话自然累积"虽优于问卷，但单次推断偏差仍大
- 评估: 方向是改进"首次规划前的画像引导"，例如：首轮规划前用几个高价值问题（过敏/忌口、烹饪方式、每周采购节奏）快速收敛，而非一次问卷；或规划后引导用户逐项确认
- 备注: 待将来讨论具体方案（2026-08-04 试用后记录）

### 关键进展

- 2026-09-13：补录编号与追溯入口；原实施状态表述为“**idea**（升级为研究问题，见下方条目）”。状态摘要现由本条独占维护，历史讨论不作为当前契约。
- 2026-10-12：首次画像需多轮纠正暂无新的失败证据，状态保持 idea，并入待办 [V-07](improvement-todo-2026-10-11.md#v-07) 的真实使用观察；出现具体问题时再按[从问题到回归用例](validation.md#from-failure-to-case)处理。

<a id="idea-004"></a>
## 库存冷启动 UX（Phase 2 重新定义）

- 编号：IDEA-004
- 状态：implemented
- 创建：2026-08-04
- 更新：2026-10-11
- 范围／完成标准：通过日常行为和轻量探测积累库存，避免首次全量盘点。
- 关联：[IDEA-007](IDEAS.md#idea-007)；[DEC-003](DECISIONS.md#dec-003)
- 实施：[70f628b](https://github.com/blizzardwj/pantry-man-skill/commit/70f628b)
- 验证与效果：历史结果未独立复验，效果待观察；[证据核对](documentation-review-2026-09-13.md#historical-evidence)。

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
- 2026-10-11：冷启动 4 轮话术规范删除，只保留“没有储备时友好地问一次”（[IDEA-031](#idea-031)、[DEC-029](DECISIONS.md#dec-029)）。

<a id="idea-005"></a>
## 研究问题：画像收敛（RQ-A / RQ-C）

- 编号：IDEA-005
- 状态：idea
- 创建：2026-08-04
- 更新：2026-10-12
- 范围／完成标准：比较画像澄清与收敛策略；研究结论不直接代表实施批准。
- 关联：[IDEA-003](IDEAS.md#idea-003)；[RQ-A](RESEARCH.md#rq-a)、[RQ-C](RESEARCH.md#rq-c)
- 实施：未实施
- 验证与效果：未实施；历史观察见下文，相关研究或修复效果尚未验证。[证据核对](documentation-review-2026-09-13.md#historical-evidence)。

### 历史背景与讨论

- 背景：由“画像收敛改进”提升而来，关注最小用户打扰与画像保真度的张力。
- 历史研究内容：问题、假设与评测方案已迁入 [RQ-A](RESEARCH.md#rq-a) 与 [RQ-C](RESEARCH.md#rq-c)；原文可由 [9457803](https://github.com/blizzardwj/pantry-man-skill/commit/9457803) 追溯。

### 关键进展

- 2026-09-13：原状态 `research` 迁到研究条目表达；实施状态归为 `idea`，未据“开展研究”推定已批准实施。原假设迁入 [RQ-A](RESEARCH.md#rq-a)、[RQ-C](RESEARCH.md#rq-c)。
- 2026-10-12：画像收敛研究（RQ-A／RQ-C 仍为 open）暂无新的失败证据，状态保持 idea，并入待办 [V-07](improvement-todo-2026-10-11.md#v-07) 的真实使用观察；出现具体问题时再按[从问题到回归用例](validation.md#from-failure-to-case)处理。

<a id="idea-006"></a>
## 每日搭配输出改进：食材搭配 + 最简便做法，而非菜谱

- 编号：IDEA-006
- 状态：implemented
- 创建：2026-08-04
- 更新：2026-09-13
- 范围／完成标准：每日搭配输出食材、价值、简便做法；后续做法原则见 DEC-010。
- 关联：[DEC-010](DECISIONS.md#dec-010)；[IDEA-012](IDEAS.md#idea-012)
- 实施：[2194b19](https://github.com/blizzardwj/pantry-man-skill/commit/2194b19)、[2143bf0](https://github.com/blizzardwj/pantry-man-skill/commit/2143bf0)
- 验证与效果：历史结果未独立复验，效果待观察；[证据核对](documentation-review-2026-09-13.md#historical-evidence)。 相关[用例定义](golden_cases/pairing_minimal_methods.json)，不代表已有通过结果。

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
- 验证与效果：历史结果未独立复验，效果待观察；[证据核对](documentation-review-2026-09-13.md#historical-evidence)。

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
- 更新：2026-10-11
- 范围／完成标准：采购计划、每日搭配独立，周计划按段编排并经确认闸门写入。
- 关联：[DEC-004](DECISIONS.md#dec-004)；前序 [IDEA-002](IDEAS.md#idea-002)
- 实施：[aaf3813](https://github.com/blizzardwj/pantry-man-skill/commit/aaf3813)
- 验证与效果：历史结果未独立复验，效果待观察；[证据核对](documentation-review-2026-09-13.md#historical-evidence)。 相关[用例定义](golden_cases/pool_hard_constraint.json)，不代表已有通过结果。

### 历史背景与讨论

- 动机: 试用 Weekly Plan 后开发者提出的 4 个问题：①清单与搭配的顺序/依赖不清（搭配应派生自清单，素材→组合）②一次输出整周清单+7天搭配信息量过大、3-4天采购对应整周搭配错位、清单写入前无确认机会 ③搭配同样需要用户参与且显示不友好（早/午/晚应列表化）④采购计划与每日搭配应拆为独立功能，周计划降为编排器
- 评估: 重构为三个模块——🛒采购计划（确认闸门：展示→确认→写入）、🍽每日搭配（食材池=已确认清单∪库存，按天分块列表显示，支持局部调整与清单联动重生成）、📆周计划（编排器：按 shoppingRhythm 切段，逐段调用前两者并逐段确认）；schema 无需变更（确认后写入即已确认，unchecked 即当前段落待购项）
- 备注: 配套决策见 DECISIONS.md [2026-08-05]；第 5 项问题（用户反馈沉淀）留作研究条目

### 关键进展

- 2026-09-13：补录编号与追溯入口；原实施状态表述为“**implemented**（commit aaf3813）”。状态摘要现由本条独占维护，历史讨论不作为当前契约。
- 2026-10-11：周计划编排器与提案持久化由 [IDEA-031](#idea-031) 收敛；采购与搭配分离、确认后才写入保留。

<a id="idea-009"></a>
## 研究问题：用户建议与反馈的沉淀、反思与再利用

- 编号：IDEA-009
- 状态：implemented
- 创建：2026-08-05
- 更新：2026-10-11
- 范围／完成标准：反馈捕获、整理与复用接入数据及计划流程；此次不修复已发现的语义缺口。
- 关联：[RQ-5](RESEARCH.md#rq-5)；[DEC-007](DECISIONS.md#dec-007)；后续 [IDEA-011](IDEAS.md#idea-011)、[IDEA-015](IDEAS.md#idea-015)
- 实施：[ba3c75b](https://github.com/blizzardwj/pantry-man-skill/commit/ba3c75b)、[9f3ead5](https://github.com/blizzardwj/pantry-man-skill/commit/9f3ead5)、[2b91c88](https://github.com/blizzardwj/pantry-man-skill/commit/2b91c88)、[76b6399](https://github.com/blizzardwj/pantry-man-skill/commit/76b6399)、[d27171b](https://github.com/blizzardwj/pantry-man-skill/commit/d27171b)、[7cb0318](https://github.com/blizzardwj/pantry-man-skill/commit/7cb0318)、[6b20ccc](https://github.com/blizzardwj/pantry-man-skill/commit/6b20ccc)、[e8b81bb](https://github.com/blizzardwj/pantry-man-skill/commit/e8b81bb)、[6e6da4d](https://github.com/blizzardwj/pantry-man-skill/commit/6e6da4d)
- 验证与效果：历史结果未独立复验，效果待观察；[证据核对](documentation-review-2026-09-13.md#historical-evidence)。 相关[用例定义](historical_cases/stock_change_deplete.json)，不代表已有通过结果。

### 历史背景与讨论

- 背景: 开发者流程分析第 5 项——用户在规划/调整中的建议和纠正是画像收敛最有价值的信号（比被动观察更直接），如何设计一套机制：保存（如何结构化记录？）、反思（何时/如何纳入画像与推荐规则？）、再利用（如何改进后续计划与搭配？）。与 RQ-A/RQ-C 画像收敛研究同源
- 备注: 完整调研与设计见 [RESEARCH.md](RESEARCH.md)；配套决策见 DECISIONS.md [2026-08-05] RQ-5 反馈机制设计；实施 = SKILL.md Feedback Capture & Reuse 章节（捕获/三层触发/闭环）+ schema.md（feedback.json + pairingTemplates + rules）

### 关键进展

- 2026-09-13：补录编号与追溯入口；原实施状态表述为“**implemented**（2026-08-05 设计并实施，commit 2b91c88..6e6da4d）”。状态摘要现由本条独占维护，历史讨论不作为当前契约。 本次审查发现的 feedback/reuse 问题集中登记于 [RQ-5](RESEARCH.md#rq-5) 的当前局限，后续另行修复。
- 2026-10-11：feedback.json 反馈机制整体取消，偏好直接写 profile，吃完以库存数量 0 表达（[IDEA-031](#idea-031)、[DEC-029](DECISIONS.md#dec-029)）；本条历史保留。

<a id="idea-010"></a>
## 采购计划数量校验：膳食指南基准 + 确认闸门前校验步骤

- 编号：IDEA-010
- 状态：implemented
- 创建：2026-08-05
- 更新：2026-09-13
- 范围／完成标准：确认闸门前按人数和天数核对建议采购量，提供软提示。
- 关联：[DEC-005](DECISIONS.md#dec-005)
- 实施：[c66baab](https://github.com/blizzardwj/pantry-man-skill/commit/c66baab)
- 验证与效果：历史结果未独立复验，效果待观察；[证据核对](documentation-review-2026-09-13.md#historical-evidence)。

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
- 更新：2026-10-11
- 范围／完成标准：提取 feedback flow，并在反馈处理和计划生成入口建立引用。
- 关联：[RQ-5](RESEARCH.md#rq-5)；[DEC-008](DECISIONS.md#dec-008)、[DEC-009](DECISIONS.md#dec-009)；前序 [IDEA-009](IDEAS.md#idea-009)
- 实施：[60e34ae](https://github.com/blizzardwj/pantry-man-skill/commit/60e34ae)
- 验证与效果：历史结果未独立复验，效果待观察；[证据核对](documentation-review-2026-09-13.md#historical-evidence)。 相关[历史用例定义](historical_cases/landing_onion_yogurt.json)已归档，代表当时规则，不是当前 golden 用例或已有通过结果。

### 历史背景与讨论

- 动机: feedback flow（Capture → Conflict avoidance → Landing decision → 三层触发 → 闭环）是 agent + skill 运行的重点，目前以散文形式嵌在 SKILL.md 正文。风险：①SKILL.md 正文越长，agent 一次载入成本越高、关键流程被浏览略过的概率越大，可靠性下降；②feedback 流程与库存/购物等常规操作性质不同——它是跨章节的状态机，理应独立
- 评估: 成本低（从 SKILL.md 移出流程文本到 `references/feedback_flow.md`，正文保留一行 citation 链接）；收益——SKILL.md 瘦身、流程可独立维护与演进、与 `references/quantity_benchmark.md` 的既有模式同构；风险——agent 必须按 citation 主动加载 reference 才能执行流程，citation 要写得明确（如"生成搭配/计划前必读"）
- 备注: 2026-08-09 真实试用暴露早餐雷同问题后讨论产出；实施时同步检查 schema.md 中 landing 定义是否随迁或互链
- 触发点模型（2026-08-09 确认）: flow 双向触发——①写侧：对话中反馈信号出现即读 flow（Capture→Conflict avoidance→Landing decision→写 feedback.json+落点文件），不经计划生成；②读侧：采购计划/每日搭配生成前读 flow（Layer 3 plan-time review：检索 active 反馈、补漏落点、耗尽候选补清单、删改≥3项时澄清）。①②同一状态机首尾，`landing.applied:false` 的记录即读侧消费的耗尽候选。因此 citation 至少出现在 SKILL.md 两处：反馈捕获章节 + 计划生成步骤
- 迁移边界（2026-08-09 确认）: Reflection triggers（三层 + Support rules）**必须整体迁入** feedback_flow.md——Layer 1=Capture、Layer 2=同日静默整理（merge/消解/升级）、Layer 3=读侧消费，三层跨写读两侧，拆出则状态机残缺。SKILL.md 反馈章节仅留概述 + 原则声明（用户数据 vs SKILL.md 分工）+ 双处 citation；schema.md 数据结构定义不动，与 flow 互链
- 术语（2026-08-09 确认）: 统一为**三层 hooks**——capture hook / threshold hook / review hook（agent 无常驻进程，整理只能挂在宿主流程自然执行点上，hooks 同时编码"何时触发"与"挂在哪里"）；见 DECISIONS.md [2026-08-09]

### 关键进展

- 2026-09-13：补录编号与追溯入口；原实施状态表述为“**implemented** (commit 60e34ae)”。状态摘要现由本条独占维护，历史讨论不作为当前契约。 本次审查发现的 feedback/reuse 问题集中登记于 [RQ-5](RESEARCH.md#rq-5) 的当前局限，后续另行修复。
- 2026-10-11：references/feedback_flow.md 已删除，内容并入 SKILL.md 基本规则与 references/planning.md（[IDEA-031](#idea-031)）。

<a id="idea-012"></a>
## SKILL.md 示例与输出解耦：示例锚定问题

- 编号：IDEA-012
- 状态：implemented
- 创建：2026-08-09
- 更新：2026-09-13
- 范围／完成标准：搭配输出示例用类别占位符表达格式，减少具体食材锚定。
- 关联：[IDEA-006](IDEAS.md#idea-006)；无独立决策条目（历史方案选择见下文）
- 实施：[e47b3c8](https://github.com/blizzardwj/pantry-man-skill/commit/e47b3c8)
- 验证与效果：历史结果未独立复验，效果待观察；[证据核对](documentation-review-2026-09-13.md#historical-evidence)。 相关[用例定义](golden_cases/dry_good_no_soup.json)，不代表已有通过结果。

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
- 更新：2026-10-12
- 范围／完成标准：明确时间戳时区格式或增加验证；尚未选择处理方案。
- 关联：无独立研究或决策；关联 [开发验证](README.md)
- 实施：未实施
- 验证与效果：未实施；历史观察见下文，相关研究或修复效果尚未验证。[证据核对](documentation-review-2026-09-13.md#historical-evidence)。

### 历史背景与讨论

- 动机: L2 黄金用例 add_inventory 首次端到端跑通时，真实 agent 把 meta.lastUpdated 写成 2026-08-13T11:23:01+0800（无冒号），而 SKILL.md Timestamp Format 与 schema.md 示例均为 +08:00（带冒号）。两者都合法 ISO 8601，但暴露「指令说 +08:00、agent 写 +0800」的 gap
- 评估: 轻微、不影响功能（dates 用 YYYY-MM-DD 是对的）。处理选项：①SKILL.md 明确要求带冒号（收紧）②schema 放宽接受两种（兼容）③断言引擎加时间戳/日期格式校验（增强 golden case，通用价值高）④不管（太轻微）。倾向 ③ 顺带做——把「时间戳/日期格式校验」作为断言引擎的通用谓词，可复用到所有涉及 bought/expires/capturedAt 的用例
- 备注: 由 dev/run_golden.py + delegate_task 端到端首跑暴露；是 golden case 价值的第一个实证（测出指令 vs 执行的细微落差，而非仅 PASS/FAIL）

### 关键进展

- 2026-09-13：补录编号与追溯入口；原实施状态表述为“idea”。状态摘要现由本条独占维护，历史讨论不作为当前契约。
- 2026-10-12：时间戳时区格式（`+08:00` 与 `+0800`）暂无新的失败证据，状态保持 idea，并入待办 [V-07](improvement-todo-2026-10-11.md#v-07) 的真实使用观察；出现具体问题时再按[从问题到回归用例](validation.md#from-failure-to-case)处理。

<a id="idea-014"></a>
## 食材咨询入口 + 通用食材知识落点

- 编号：IDEA-014
- 状态：implemented
- 创建：2026-08-15
- 更新：2026-09-13
- 范围／完成标准：新增独立食材咨询及通用知识引用，复用用户画像。
- 关联：[DEC-012](DECISIONS.md#dec-012)
- 实施：[f8e9455](https://github.com/blizzardwj/pantry-man-skill/commit/f8e9455)、[b1557d4](https://github.com/blizzardwj/pantry-man-skill/commit/b1557d4)
- 验证与效果：旧 DEC-012 记载 static validation PASS，但未找到该次执行报告；效果待观察。[证据核对](documentation-review-2026-09-13.md#historical-evidence)。

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
- 验证与效果：历史结果未独立复验，效果待观察；[证据核对](documentation-review-2026-09-13.md#historical-evidence)。

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
- 验证与效果：历史结果未独立复验，效果待观察；[证据核对](documentation-review-2026-09-13.md#historical-evidence)。

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
- 验证与效果：[本次验证](documentation-review-2026-09-13.md#documentation-checks)；文档检查不代表反馈业务验证，长期维护效果待观察。

### 关键进展

- 2026-09-13：用户确认先完成四项文档治理，再处理 feedback/reuse；按此范围完成文档整理，保留原始设计供下一步复核。
- 2026-10-02：三文件位置由根目录移至 `dev/`，职责分工不变；见后续 [IDEA-022](#idea-022)。本项原完成范围不变。

<a id="idea-018"></a>
## 反馈事实落点与耗尽候选生命周期分离

- 编号：IDEA-018
- 状态：implemented
- 创建：2026-09-28
- 更新：2026-10-11
- 问题与预期结果：applied 同时表示落点完成与待补货候选；需分开事实变更与选品参考，避免普通不买／删清单被过度解读。
- 范围／完成标准：运行契约覆盖多落点、逐食材耗尽与补货、跨日选择性参考、普通删清单不改变耗尽事实、补货逐项 decay；确认建议删 ≥3 项时先执行删改、本次补问一次，按真实回答处理，未回答不猜测、不追问。字段、各入口步骤与同轮已问识别落入 SKILL.md 及 references；开发版旧反馈不迁移，仅定义归档重建行为，不执行真实数据清理。
- 关联：[耗尽记录说明](RESEARCH.md#rq-5-depletion-simplified)、[补问说明与验收场景](RESEARCH.md#rq-5-clarification-once)、[早期比较](RESEARCH.md#rq-5-depletion-proposal)；前序 [IDEA-009](#idea-009)、[IDEA-011](#idea-011)，后续 [IDEA-020](#idea-020) 的反馈边界与恢复机制替代、[IDEA-021](#idea-021) 的购买语义调整；当时决策 [DEC-017](DECISIONS.md#dec-017)、[DEC-018](DECISIONS.md#dec-018)、[DEC-019](DECISIONS.md#dec-019)，后续替代见 [DEC-021](DECISIONS.md#dec-021)。
- 实施：[3e6d1bd](https://github.com/blizzardwj/pantry-man-skill/commit/3e6d1bd) 实施当时的 SKILL、feedback_flow、schema、README 和开发样例；未执行真实用户数据清理。其 `landings[]` 写前／恢复部分已由 IDEA-020 替代，耗尽选择性复用继续适用。
- 验证与效果：[本次验证记录](feedback-refactor-review-2026-09-28.md)：仓库静态检查、作者执行的两个 golden 用例及部分回购／中断／补问数据检查通过；skill-creator 验证器缺 PyYAML 未运行。独立 agent 行为回归与长期效果尚未验证。

### 关键进展

- 2026-09-28：用户指出审查问题 1、2 同源，要求先分析修改方案；记录三个候选及暂定倾向，保持 idea，未将研究授权视为实施批准。
- 2026-09-28（后续澄清）：按用户明确的四项选择收敛为“耗尽事实保留、采购时选择性参考、买回逐项 decay、开发版无需兼容旧反馈”；记录 DEC-017。删除早期方案的普通拒购状态与旧格式迁移要求，历史论证留在 RQ-5；尚未开始行为实现或数据清理。
- 2026-09-28（第二部分确认）：按用户要求将补问解答记入 RQ-5 和 DEC-018，保留旧“下次补问”的历史。明确本次只问一次、分别处理真实回答、未回答不猜测也不追问；记录后续验收场景，保持 idea，尚未实施运行行为或执行业务测试。
- 2026-09-28（开始实施）：用户已提交设计文档并明确要求重构三个运行文件；转为 implementing，按已接受的两项决策落实字段、入口和验证，不执行真实用户数据清理。
- 2026-09-28（完成本轮范围）：运行契约与开发样例已更新，转为 implemented；静态检查和作者执行的关键场景结果见[验证记录](feedback-refactor-review-2026-09-28.md)。提交待用户安排；独立 agent 回归与长期效果仍待观察，不将文字规则完成等同于所有宿主已验证。
- 2026-09-29：用户进一步质疑把普通购买写为反馈的消费价值；新的输入边界研究由 [IDEA-020](#idea-020) 承接，本项已完成范围及其历史结果不变。
- 2026-09-29：用户指出普通“买了苹果”应按个人购物清单的日常语义勾选；该独立调整由 [IDEA-021](#idea-021) 承接，不更改本项的历史完成范围。
- 2026-09-30：[IDEA-020](#idea-020) 和 [DEC-021](DECISIONS.md#dec-021) 移除了本项中的写前／恢复部分，保留逐食材耗尽信号与选择性补购；当时实现和验证仍由上述提交及报告追溯。
- 2026-10-11：耗尽候选生命周期改为跟随库存条目（数量 0 → 补货写入新数量），不再需要跨文件失效判断（[IDEA-031](#idea-031)、[DEC-029](DECISIONS.md#dec-029)）。

<a id="idea-019"></a>
## 语音输入条件下的范围收敛与核心流程改进

- 编号：IDEA-019
- 状态：implemented
- 创建：2026-09-28
- 更新：2026-10-12
- 问题与预期结果：外部 review 对录入负担的判断未充分考虑宿主语音输入；需要收敛扩张范围，优先修复用户已表达的信息未正确应用、搭配依赖和状态混淆问题。
- 范围／完成标准：当前仅交付[收敛与改进建议](convergence-review-2026-09-28.md)。候选改动按重要性及相对成本排序，每项列最小范围和验收场景；行为实施须另行确定批次，不能把文档完成视为这些改动完成。
- 关联：前序 [IDEA-008](#idea-008)、[IDEA-004](#idea-004)；反馈生命周期由 [IDEA-018](#idea-018) 跟踪，方案见 [RQ-5](RESEARCH.md#rq-5-depletion-proposal)，不重复维护其进展。本项无新增研究或设计决策。
- 实施：建议文档已见 [3a1628b](https://github.com/blizzardwj/pantry-man-skill/commit/3a1628b)；本条其他候选行为未因此实施。反馈边界改动另由 [IDEA-020](#idea-020) 跟踪。
- 验证与效果：建议基于 2026-09-28 当时的运行契约对照，场景均为待验收条件；未执行业务测试或语音效果评测，实际收益待观察。反馈相关候选的后续验证见 [IDEA-020](#idea-020)。

### 关键进展

- 2026-09-28：用户要求形成高信息密度的收敛与改进文档，并明确语音已降低输入负担；据此将近期重点放在已有输入的可靠应用和核心使用路径，暂缓新 Capture 渠道及高级机制扩张建议，未更改运行契约。
- 2026-09-30：建议文档的反馈相关部分已有 [IDEA-020](#idea-020) 后续实现；本条其余候选仍保持 idea，不把历史建议当作当前运行契约。
- 2026-10-11：候选 1（每日搭配食材池）、候选 2（过期删除）列入 [待办清单](improvement-todo-2026-10-11.md) 的 F-01、F-02，排入第一批；进展仍由本条维护，状态不变。
- 2026-10-11：用户要求开始修复 F-01；候选 1 拆为 [IDEA-024](#idea-024) 实施并由其维护进展（同 IDEA-020 承接反馈部分的做法）。本条其余候选仍为 idea。
- 2026-10-11：用户要求修复 F-02；候选 2 拆为 [IDEA-025](#idea-025) 实施并由其维护进展。本条其余候选（3、5、6）仍为 idea。
- 2026-10-11：候选 3（反馈 importance 与明确操作边界）随 [IDEA-031](#idea-031) 取消反馈机制而不再适用；候选 5、6 仍为 idea。
- 2026-10-12：收尾复核：本条范围（交付收敛建议文档，见 3a1628b）早已完成，候选均已有去向——1 → [IDEA-024](#idea-024)，2 → [IDEA-025](#idea-025)，3 随反馈机制取消不再适用（[IDEA-031](#idea-031)），4 → [IDEA-020](#idea-020)／[IDEA-031](#idea-031)，5 由基本规则 1 与 schema“未知不为 0、不编造”覆盖（[IDEA-031](#idea-031)），6 → 冷启动简化（[IDEA-031](#idea-031)）与 README 重新定位（[IDEA-023](#idea-023) 的 A-01）。转为 implemented。

<a id="idea-020"></a>
## 用户输入进入反馈的边界：业务操作与可复用反馈分离

- 编号：IDEA-020
- 状态：implemented
- 创建：2026-09-29
- 更新：2026-10-11
- 问题与预期结果：普通购买、已有库存及一次性清单操作曾与可复用个性化信号混写在 `feedback.json`，且每次操作都承担中断恢复记录。按用户本轮说明，普通 CRUD 直接更新业务文件；明确消费至耗尽则同时留下选择性补购信号。
- 范围／完成标准：Capture 用表格明确普通购买、已有、消费完、丢弃、清单操作、偏好和搭配评价的分界；当前购买更新 pantry/shopping/history 而不新建反馈，旧耗尽信号逐项结束；删除运行契约中的 `landings[]` 写前和恢复流程，CRUD 直接落业务文件；schema、README、开发样例同步；保留现有 v2 历史数据但不执行旧操作字段。采购计划仍选择性复用消耗信号，不据吃完自动判定长期喜爱。
- 关联：[RQ-7](RESEARCH.md#rq-7)；前序 [IDEA-018](#idea-018)；新决策 [DEC-021](DECISIONS.md#dec-021)，部分替代 [DEC-019](DECISIONS.md#dec-019) 的恢复机制，保留 [DEC-017](DECISIONS.md#dec-017) 的选择性耗尽复用。
- 实施：[359b981](https://github.com/blizzardwj/pantry-man-skill/commit/359b981) 同步 SKILL、feedback_flow、schema、README 和开发样例／用例；未改动真实用户数据。Capture 边界列的后续明确化见当前工作区／尚未提交。
- 验证与效果：[2026-09-30 关联文档复核](feedback-alignment-review-2026-09-30.md)：`dev/validate_static.py` 通过（0 FAIL，1 项既有 `cron add` 占位警告），26 份开发 JSON 解析通过，14 份 Git 跟踪 Markdown 的本地链接／显式锚点检查及 `git diff --check` 通过。定向用例定义覆盖普通入库／购买不新增反馈、明确偏好入反馈、耗尽及补货后旧信号结束。用例定义不等于独立 agent 执行；实际行为和长期效果待观察。

### 关键进展

- 2026-09-29：用户指出“买了什么”是普通入库事实，不表达偏好变化或对既有记忆的纠正；要求研究用户输入进入 feedback 的边界。启动 [RQ-7](RESEARCH.md#rq-7)，不把讨论当成实施批准。
- 2026-09-30：用户明确要求用表格定反馈边界，保留“吃完了”的消费与可能复购信号，移除数据更新／中断恢复机制，先收敛基本 CRUD 与反馈逻辑；据此转为 implementing。
- 2026-09-30：运行契约、schema、用户文档和开发用例已按 [DEC-021](DECISIONS.md#dec-021) 更新；静态与 JSON 检查通过，转为 implemented。保留已有 v2 记录，不把旧写入进度作为任务执行；独立 agent 行为回归尚未完成。
- 2026-09-30（文档对齐）：Capture 表单列标明“是否属于 feedback”及理由，并把消费去向放在独立一列；当前工作区／尚未提交。此次是表达方式澄清，不更改 DEC-021 的边界。
- 2026-09-30（关联文档复核）：对齐 RQ-5/RQ-7 当前摘要、DEC-017 后续关系、IDEAS 提交链接及开发用例／样例；历史报告注明旧契约范围。检查结果见[复核记录](feedback-alignment-review-2026-09-30.md)，当前工作区／尚未提交。
- 2026-10-11：反馈日志取消，业务操作与偏好分离的边界保留为 SKILL.md 基本规则（[IDEA-031](#idea-031)、[DEC-029](DECISIONS.md#dec-029)）。

<a id="idea-021"></a>
## 日常购买报告默认完成对应购物项

- 编号：IDEA-021
- 状态：implemented
- 创建：2026-09-29
- 更新：2026-09-30
- 问题与预期结果：现行购买步骤要求先确认是否买足，导致“买了苹果”仍可能留在个人待购清单中；按日常使用习惯默认完成对应项，保留明确部分购买或补记旧账的例外。
- 范围／完成标准：SKILL.md 与 feedback_flow.md 一致规定当前“买了某物”默认勾选匹配待购项，不要求报数量；schema 说明 checked 的含义；明确部分购买、仍需再买及历史补记不误勾选。当时要求实际数量、日期、价格未知时不编造；后续 [IDEA-020](#idea-020) 明确反馈准入及“当前购买按本地当天记账、历史日期不清不记到今天”的日期语义。
- 关联：前序 [IDEA-018](#idea-018)；[DEC-020](DECISIONS.md#dec-020)；反馈准入另见 [IDEA-020](#idea-020)。无需新增研究条目。
- 实施：[359b981](https://github.com/blizzardwj/pantry-man-skill/commit/359b981) 包含购买默认勾选的运行规则、schema 和 README；当时未单独提交。后续购买与反馈分离见 [IDEA-020](#idea-020)。
- 验证与效果：2026-09-29 运行 `dev/validate_static.py`，0 FAIL、1 项既有 `cron add` 占位警告；`git diff --check` 通过。定向核对“买了苹果”默认勾选、明确部分购买保留待购、历史补记不勾选三种文本规则，以及新锚点链接。尚未执行独立 agent 行为回归，实际使用效果待观察。

### 关键进展

- 2026-09-29：用户明确个人助手无需按商业库存盘点方式核对购买量，要求遵循“买了苹果”即完成对应清单项的日常语义；开始实施，保留明确部分购买的例外。
- 2026-09-29：运行契约、schema 与 README 已同步，转为 implemented；验证覆盖静态结构和规则一致性，未将文档检查视为实际 agent 行为验证。
- 2026-09-30：[DEC-021](DECISIONS.md#dec-021) 保留本项的勾选语义，并另行规定购买不产生新反馈及当前购买日期的默认处理；本项原有完成范围和验证记录保留。

<a id="idea-022"></a>
## 开发演进记录移入 dev/：与 skill 运行文件分开

- 编号：IDEA-022
- 状态：implemented
- 创建：2026-10-02
- 更新：2026-10-02
- 问题与预期结果：IDEAS／DECISIONS／RESEARCH 只供开发 agent 维护，却与 SKILL.md 并列在根目录，容易被当作 skill 运行内容。移入 `dev/` 后，根目录只保留 skill 契约、用户文档和开发入口 AGENTS.md。
- 范围／完成标准：三文件以 `git mv` 移入 `dev/` 保留历史；其中指向根目录文件和 `dev/` 的相对链接、dev 下复核报告指向三文件的链接全部改写并可解析；AGENTS.md 目录结构与工作流路径、dev/README.md 内容清单同步；不改动 SKILL.md、references 及运行行为。不包括调整安装分发范围（见 DEC-022 局限）。
- 关联：[DEC-022](DECISIONS.md#dec-022)；前序 [IDEA-017](#idea-017)、[DEC-016](DECISIONS.md#dec-016)。无独立研究条目。
- 实施：[383c318](https://github.com/blizzardwj/pantry-man-skill/commit/383c318)
- 验证与效果：2026-10-02 对所有 Git 跟踪 Markdown 做本地链接与显式锚点检查，0 处失效；`dev/validate_static.py` 通过（0 FAIL，1 项既有 `cron add` 占位警告）；`git diff --check` 通过；Git 将三文件识别为重命名，历史可追溯。GitHub 等外部位置指向旧根目录路径的链接会失效，未做处理。

### 关键进展

- 2026-10-02：用户确认三文件面向开发 agent 而非 Hermes 等运行时 agent，决定移入 `dev/`；转为 implementing，完成移动、链接改写与 AGENTS.md／dev/README.md 同步后转为 implemented。

<a id="idea-023"></a>
## 修复、价值提升与扩大使用待办清单

- 编号：IDEA-023
- 状态：implementing
- 创建：2026-10-11
- 更新：2026-10-12
- 问题与预期结果：2026-10-11 技术评估认为，运行契约在事实与推断区分上质量较高，但存在已知未修矛盾（搭配食材池、过期删除、宿主专属调度、品类归类）、缺失状态（规划时段、itemKey 一致性、派生 status）、单次操作指令量过大，以及价值削弱因素（数据绑定单一 agent、带作者个人画像、宿主定位不符、缺少执行与对比证据）。需要一份按投入产出排序的待办，作为后续批次实施的范围依据。
- 范围／完成标准：当前仅交付[待办清单](improvement-todo-2026-10-11.md)：修复（F-01～F-08）、价值提升（V-01～V-07）、扩大使用（A-01～A-06），每项含最小范围、验收场景、相对投入和依赖，并给出建议批次。行为实施须由用户另行确定批次后转 planned；清单完成不代表任何条目已实施。
- 关联：F-01、F-02 即 [IDEA-019](#idea-019) 候选 1、2；F-01、F-02 已分别拆为 [IDEA-024](#idea-024)、[IDEA-025](#idea-025)；V-07 承接[收敛建议 §4](convergence-review-2026-09-28.md)。V-02 实施前需新增 DEC，V-03 需新增 RQ。前序 [IDEA-020](#idea-020)、[IDEA-021](#idea-021)。
- 实施：待办清单见 [cb61d54](https://github.com/blizzardwj/pantry-man-skill/commit/cb61d54)；各条目实施由相应 IDEA 跟踪（F-01 见 [IDEA-024](#idea-024)，F-02 见 [IDEA-025](#idea-025)，F-03 见 [IDEA-026](#idea-026)，F-04 见 [IDEA-027](#idea-027)，F-05 见 [IDEA-028](#idea-028)，F-06 见 [IDEA-029](#idea-029)）。
- 验证与效果：清单依据为契约对照与行号核对，未执行 agent 行为测试；本次环境无可用 Python，`dev/validate_static.py` 未运行。各项收益为项目判断，待对应验收与 A-03、V-06 证据确认。

### 关键进展

- 2026-10-11：用户要求在技术评估基础上建立待办清单，覆盖主要问题修复、价值削弱因素修复及按投入产出比排序的扩大使用工作；新建清单，状态为 idea，尚未决定实施批次。
- 2026-10-11：F-07 经讨论放弃（[IDEA-030](#idea-030)）：跨会话续接时段的场景低频，以当天日期推算即可满足多数情况，新增字段与分支与收敛方向相反。用户随后确认 V-01、V-02 优先于 F-08、A-02，并选择反馈方案 B，由 [IDEA-031](#idea-031) 实施；F-08 待收敛后的使用情况再评估。
- 2026-10-11：按 DEC-029 收敛后的契约逐项复核待办，见[复核](improvement-todo-2026-10-11.md#review-2026-10-11)：F-01～F-06、V-01、V-02 范围已覆盖，F-07、F-08 失效（F-08 转观察项），V-04 基本已覆盖，A-02、V-05 范围缩小并搁置；以三阶段计划替代初版批次，当前主线为 V-07 实际使用与 A-03 运行核心用例。
- 2026-10-11：`validate_static.py` 首次在本机运行通过（FAIL 0、WARN 0），runner 新增的 null fixture、`exists`、`contains_any` 及数量路径断言经无 agent 自测符合预期；golden case 仍未经 agent 执行，A-03 剩余部分为把 delegation_prompt 交给 agent 执行。
- 2026-10-11：A-03 首轮完成：Claude Code + Haiku 执行全部 19 个用例，15/19 通过，失败经 [IDEA-032](#idea-032) 修复后重跑 8/8 通过；执行脚本 `dev/run_cases_claude.ps1`，见 [执行报告](golden-run-2026-10-11.md)。跨宿主执行与多次重复稳定性仍未做。
- 2026-10-12：A-04 完成：README 以“Recommended Hosts”推荐带语音输入、可从手机／聊天访问、可定时的个人助理型 agent（如 Hermes），编码类 agent 说明为试用与开发测试用；新增“一句话多项操作”语音示例，并用新用例 `voice_multi_op`（买了牛奶菠菜、鸡蛋吃完、过期酸奶扔了）以 Claude Code + Haiku 执行 3 次，3/3 PASS，见[执行报告](golden-run-2026-10-11.md#addendum-2026-10-12)。仅改 README，SKILL.md 保持宿主无关；已提交 [a825a58](https://github.com/blizzardwj/pantry-man-skill/commit/a825a58)。
- 2026-10-12：新增交互测试（现为 [验证方案 L3](validation.md#l3)）作为第三种验证方式（用户直接与宿主 agent 对话），覆盖宿主内手动复现用例、触发测试、日常使用观察（快照对比、检查清单、使用记录与四类归因），以及把实际问题转成回归用例的流程；作为 V-07 的执行方法，可在 Hermes + deepseek-flash 等宿主与模型上复用。已提交 [a825a58](https://github.com/blizzardwj/pantry-man-skill/commit/a825a58)。
- 2026-10-12：A-04 扩展为语音与拍照输入，由 [IDEA-033](#idea-033) 实施（[DEC-030](DECISIONS.md#dec-030)）；README 推荐宿主与示例同步。
- 2026-10-12：A-01 完成：README 开头改为“根据家里现有食材规划买什么、怎么吃”（附中文一句），Features 分为“Plan from what you have”与“Kept up to date as you go”，Usage 按规划／记录分组并给出中英示例；食材咨询示例改为带画像的说法以符合收窄后的触发描述。仅文档改动。V-05 由 [IDEA-034](#idea-034) 实施。已提交 [9437f4c](https://github.com/blizzardwj/pantry-man-skill/commit/9437f4c)。
- 2026-10-12：全面检查：提交 9437f4c 上全量 28 用例 27/28（唯一失败为 en_add_keeps_name 的间歇性名称翻译，累计 7/8）；静态校验与链接检查通过；IDEAS 中 7 处“本次工作区／尚未提交”已补为实际提交链接。剩余待办见待办清单复核与本条后续记录。
- 2026-10-12：状态由 idea 转为 implementing：待办清单已交付，A-01、A-04、V-01、V-02、V-05、F-01～F-06 等已实施，A-03 部分完成，其余项按复核的阶段计划推进。
- 2026-10-12：按全面检查结果完成快速整理（IDEA-019 关闭、IDEA-003／005／013 并入 V-07 观察、本条转 implementing、validation.md 增加术语说明），并由 [IDEA-035](#idea-035) 补齐测试覆盖缺口。用例总数 35。

<a id="idea-024"></a>
## 每日搭配食材池按用餐时点区分（待办 F-01）

- 编号：IDEA-024
- 状态：implemented
- 创建：2026-10-11
- 更新：2026-10-11
- 问题与预期结果：原契约把未购清单条目算入每日搭配食材池，且清单为空时拒绝“今晚吃什么”。预期当天用餐只用现有库存且不被采购流程阻塞；提前规划可使用已确认待买项并明确标注。
- 范围／完成标准：按 [待办 F-01](improvement-todo-2026-10-11.md#f-01)。SKILL.md 每日搭配定义当下用餐／时段规划两种模式及各自食材池、清单为空与库存不足时的处理、待买标记，周计划第 3b 步指定时段规划；feedback_flow.md Review 第 4 条与 README 示例同步；新增覆盖两种模式的 golden case。不含 schema 时段字段（F-07）和过期删除规则修正（F-02）。
- 关联：[DEC-023](DECISIONS.md#dec-023)（部分替代 [DEC-004](DECISIONS.md#dec-004)）；前序 [IDEA-019](#idea-019) 候选 1、[IDEA-023](#idea-023)；无新增研究条目。
- 实施：[3ebf6c2](https://github.com/blizzardwj/pantry-man-skill/commit/3ebf6c2)。改动：SKILL.md（Meal Planning 概述、每日搭配食材池与流程、周计划 3b）、references/feedback_flow.md（④ Review 第 4 条）、README.md（功能与示例描述）；开发侧新增 fixture `pairing_stock`、`pairing_stock_pending`，golden case `pairing_meal_now_empty_list`、`pairing_meal_now_stock_only`、`pairing_segment_pending_marked`，断言引擎新增文本谓词 `contains_any`。
- 验证与效果：2026-10-11 用 Node 解析新增 fixture 与 golden case JSON 通过；人工核对 SKILL.md、feedback_flow.md、schema.md 中食材池相关表述一致（schema 中“草稿不进入食材池”不变）。本次环境无可用 Python，`dev/validate_static.py` 与 `run_golden.py` 未运行，`contains_any` 改动未经执行；三个新 golden case 未交给独立 agent 执行，模式判断准确率与实际使用效果待观察。

### 关键进展

- 2026-10-11：用户要求开始修复待办 F-01；从 IDEA-019 候选 1 拆出，按 [DEC-023](DECISIONS.md#dec-023) 实施，约定范围完成后转为 implemented（验证缺口见上）。
- 2026-10-11（验证补记）：`contains_any` 谓词用手写 response.txt 自测 PASS（`pairing_meal_now_empty_list`）；skill 行为仍未经 agent 执行。

<a id="idea-025"></a>
## 过期条目保留并询问处置（待办 F-02）

- 编号：IDEA-025
- 状态：implemented
- 创建：2026-10-11
- 更新：2026-10-11
- 问题与预期结果：SKILL.md 定期清理任务按过期日期直接删除库存条目，与“过期不证明消耗”矛盾。预期过期条目仍可查到并标为已过期、不进入搭配食材池，只在用户说明吃完、扔了或还在后更新。
- 范围／完成标准：按 [待办 F-02](improvement-todo-2026-10-11.md#f-02)。SKILL.md 查看库存与过期检查标出已过期，新增 Expired items 处置规则，库存感知中的过期提醒与之对齐，Heartbeat 清理任务改为提醒并询问、不写文件；feedback_flow.md Capture 表增加“已过期但未说明处置”一行；schema.md `expires` 说明与 README 同步；新增覆盖“查看时保留”和“扔了后移除且无反馈”的 golden case。不含 `status` 字段存储方式（F-06）与定时任务宿主无关化（F-03）。
- 关联：[DEC-024](DECISIONS.md#dec-024)；前序 [IDEA-019](#idea-019) 候选 2、[IDEA-023](#idea-023)；与 [IDEA-024](#idea-024) 的“过期不进食材池”一致；无新增研究条目。
- 实施：[d61cfa8](https://github.com/blizzardwj/pantry-man-skill/commit/d61cfa8)。改动：SKILL.md（View by zone、Check expiry、新增 Expired items、Stock grows 中的过期提醒、Heartbeat 改为 Expired Items Review）、references/feedback_flow.md（Capture 表）、references/schema.md（`expires` 说明）、README.md（Expiry Tracking）；开发侧新增 fixture `expired_milk`，golden case `expired_kept_on_view`、`expired_discarded`。
- 验证与效果：2026-10-11 用 Node 解析新增 fixture 与 golden case JSON 通过；人工核对 SKILL.md、feedback_flow.md、schema.md 中删除／过期相关表述不再包含按日期删除的规则。本次环境无可用 Python，`dev/validate_static.py` 与 `run_golden.py` 未运行；新 golden case 未交给独立 agent 执行，“询问一次”的执行情况与实际效果待观察。过期条目不进食材池的场景未单独建用例（回复中可能合理提及“牛奶已过期”，文本断言难以区分）。

### 关键进展

- 2026-10-11：用户要求修复待办 F-02；从 IDEA-019 候选 2 拆出，按 [DEC-024](DECISIONS.md#dec-024) 实施，约定范围完成后转为 implemented（验证缺口见上）。

<a id="idea-026"></a>
## 定时提醒宿主无关化（待办 F-03）

- 编号：IDEA-026
- 状态：implemented
- 创建：2026-10-11
- 更新：2026-10-11
- 问题与预期结果：SKILL.md 提醒章节使用 `cron add` 与 `HEARTBEAT.md`，数据路径缺 `[AGENT_HOME]`，违反硬规则 #1；静态校验长期保留 1 项 WARN。预期提醒能力保留，任何宿主都能按语义执行，且校验能阻止此类写法再次出现。
- 范围／完成标准：按 [待办 F-03](improvement-todo-2026-10-11.md#f-03)。SKILL.md 的 Scheduled Reminders 与 Heartbeat Tasks 合并为宿主无关的提醒表（含过期条目提醒、只读约束、创建前征得同意、按用户本地时区），路径统一带 `[AGENT_HOME]`；`dev/validate_static.py` 对宿主专属调度写法和未锚定的数据路径报 FAIL。不改变提醒文案语言（属 V-05）。
- 关联：[DEC-025](DECISIONS.md#dec-025)（整项替代 [DEC-006](DECISIONS.md#dec-006)）；[IDEA-025](#idea-025) 的过期提醒语义保留；[IDEA-023](#idea-023)；无新增研究条目。
- 实施：[ea26391](https://github.com/blizzardwj/pantry-man-skill/commit/ea26391)。改动：SKILL.md（Scheduled Reminders 重写、删除 Heartbeat Tasks 小节）、dev/validate_static.py（检查 [4] 规则）。
- 验证与效果：2026-10-11 用 `grep -P` 以与新校验等价的正则预检 SKILL.md 与 references/*.md：无 `cron add`／`HEARTBEAT.md`，无缺 `[AGENT_HOME]` 的 `pantry/data` 路径。本次环境无可用 Python，`dev/validate_static.py` 未运行，待办 F-03 的“0 FAIL、0 WARN”验收尚无执行证据。宿主实际创建定时任务的行为未验证。

### 关键进展

- 2026-10-11：用户要求修复待办 F-03；按 [DEC-025](DECISIONS.md#dec-025) 实施，约定范围完成后转为 implemented（验证缺口见上）。
- 2026-10-11（验证补记）：用户在本机 conda Python 运行 `python dev/validate_static.py`，基于提交 dd69d90（工作区另有仅文档改动）：FAIL 0、WARN 0，检查 [4] 的宿主命令与未锚定路径规则首次执行通过；待办 F-03 的“0 FAIL、0 WARN”验收达成。agent 复跑同一结果。

<a id="idea-027"></a>
## 运行文档内矛盾清理（待办 F-04）

- 编号：IDEA-027
- 状态：implemented
- 创建：2026-10-11
- 更新：2026-10-11
- 问题与预期结果：运行文档之间存在归类与引用矛盾：SKILL.md 采购计划示例表把青椒、黄瓜列在“水果”，而 quantity_benchmark.md 归“蔬菜”；SKILL.md 的“蛋白质”“主食”展示类别与基准的“鱼禽肉蛋／豆制品”“谷类主食／薯类”未说明对应关系；示例中的香菇、海带及 ingredient_knowledge.md 中的鲜豆类、莲藕在基准归类规则中缺失；schema.md 免责声明指向不存在的“Weekly Plan section”，画像确认时机写成“首个周计划后”，与 SKILL.md“首个生成的计划后”不一致。预期同一食材在各文件中归类一致，交叉引用可解析。
- 范围／完成标准：按 [待办 F-04](improvement-todo-2026-10-11.md#f-04)。SKILL.md 示例表品类以 quantity_benchmark 为准并说明展示类别与基准类别的对应，数量校验步骤写明按基准归类、无日参考范围的类别（油脂、坚果）不校验；quantity_benchmark.md 补鲜豆类、菌藻（干鲜口径分开）、莲藕的归类；schema.md 修正两处引用与表述。不新增营养基准数值（如油脂、坚果日参考量）。
- 关联：沿用 [DEC-005](DECISIONS.md#dec-005)（数量校验）与 [DEC-015](DECISIONS.md#dec-015)（纤维口径）的既有规则，本项为一致性修正，无新增决策或研究条目；[IDEA-023](#idea-023)。
- 实施：[f1338fb](https://github.com/blizzardwj/pantry-man-skill/commit/f1338fb)。改动：SKILL.md（采购计划示例表及说明、第 7 步数量校验）、references/quantity_benchmark.md（Category Assignment Rules）、references/schema.md（profile 说明、免责声明引用）。
- 验证与效果：2026-10-11 人工核对 SKILL.md、quantity_benchmark.md、ingredient_knowledge.md 中青椒、黄瓜、鲜豆类、菌藻、莲藕的归类一致，SKILL.md 各级标题与 references 中对 SKILL.md 小节的引用（Expired items、Inventory Awareness、User Profile、⚠️ Health Disclaimer）均存在。本次环境无可用 Python，`dev/validate_static.py` 未运行；数量校验输出未经 agent 执行验证，未新增 golden case（校验报告为自由文本，现有断言难以精确判断归类）。干品菌藻“不按干重计入蔬菜目标”是依据 DEC-015 口径规则作出的项目推断。

### 关键进展

- 2026-10-11：用户要求修复待办 F-04；按上述范围实施并转为 implemented（验证缺口见上）。核对中另发现 schema.md 画像确认时机与 SKILL.md 不一致，一并修正。

<a id="idea-028"></a>
## 首次写入前才初始化、收窄触发描述（待办 F-05）

- 编号：IDEA-028
- 状态：implemented
- 创建：2026-10-11
- 更新：2026-10-11
- 问题与预期结果：description 覆盖一般烹饪提问，First-Run Setup 要求任何请求前先建数据目录，误触发或只读请求都会在 agent home 留下数据文件。预期与用户库存无关的提问不触发或不留数据，首次写入仍能无感初始化。
- 范围／完成标准：按 [待办 F-05](improvement-todo-2026-10-11.md#f-05)。SKILL.md description 以用户自有库存／清单／购买／画像为中心并排除一般菜谱问题；First-Run Setup 区分只读（缺失按空种子回答、不创建）与首次写入前初始化，回执与写入结果合并；食材咨询仅在 profile.json 存在时读取。开发侧 runner 支持无数据目录的首次场景（`"fixture": null`）与文件级 `exists` 断言，新增三个首次使用用例。
- 关联：[DEC-026](DECISIONS.md#dec-026)（部分替代 [DEC-001](DECISIONS.md#dec-001)）；前序 [IDEA-001](#idea-001)、[IDEA-023](#idea-023)；无新增研究条目。
- 实施：[e084baf](https://github.com/blizzardwj/pantry-man-skill/commit/e084baf)。改动：SKILL.md（frontmatter description、First-Run Setup、食材咨询第 2 步）；dev/run_golden.py（`setup_fixture` 支持 null、`run_assertions` 支持 `exists`）、dev/README.md；golden case `first_run_consult_no_init`、`first_run_view_no_init`、`first_run_add_initializes`。
- 验证与效果：2026-10-11 Node 解析新增用例 JSON 通过；description 710 字符（规范上限 1024），frontmatter 仍为单行 `name`／`description`。本次环境无可用 Python，`dev/validate_static.py` 与修改后的 `run_golden.py` 均未运行；新用例未交给独立 agent 执行。宿主是否按新 description 减少误触发未测试；用例中的执行者被直接要求使用本 skill，只能验证触发后的只读无副作用，不能验证触发判断。

### 关键进展

- 2026-10-11：用户要求修复待办 F-05；按 [DEC-026](DECISIONS.md#dec-026) 实施，约定范围完成后转为 implemented（验证缺口见上）。
- 2026-10-11（验证补记）：用 conda Python 自测修改后的 `run_golden.py`（不经 agent）：`first_run_view_no_init` prepare 后数据目录不存在、三项 `exists: false` 断言 PASS；`first_run_add_initializes` 未写入时 `exists: true` 与内容断言按预期 FAIL。这只验证 runner 与断言本身，skill 行为仍未经 agent 执行。

<a id="idea-029"></a>
## 库存过期状态读取时计算（待办 F-06）

- 编号：IDEA-029
- 状态：implemented
- 创建：2026-10-11
- 更新：2026-10-11
- 问题与预期结果：库存条目存储 `status`（fresh / expiring_soon / expired），没有流程随日期更新，存储值会过时并与 `expires` 矛盾。预期过期状态始终按日期正确显示，无需人工或定时更新。
- 范围／完成标准：按 [待办 F-06](improvement-todo-2026-10-11.md#f-06)。SKILL.md 新增 Expiry state 计算规则（已过期／即将过期，默认 3 天），查看库存与过期检查引用它，禁止为库存条目写 `status`、旧值忽略不回写；schema.md 将 `status` 标为 legacy；schema 黄金样例按当前写入约定更新；新增“旧 status 与日期矛盾”用例。不迁移或清理用户旧数据。
- 关联：[DEC-027](DECISIONS.md#dec-027)；与 [IDEA-025](#idea-025)（过期保留并询问）配合；[IDEA-023](#idea-023)；无新增研究条目。
- 实施：[7460054](https://github.com/blizzardwj/pantry-man-skill/commit/7460054)。改动：SKILL.md（View by zone、Check expiry、新增 Expiry state）、references/schema.md（pantry 条目 `status` 行）；dev/schema_probe/pantry.json（去掉 `status`，补上必填的 `itemKey`）；新增 fixture `stale_status`（牛奶 `expires` 2026-10-01 但 `status` 为 fresh）与 golden case `stale_status_ignored`。现有 fixture 中的 `status` 作为旧数据保留，用于兼容读取。
- 验证与效果：2026-10-11 Node 解析修改后的 schema 样例、新 fixture 与用例 JSON 通过；人工核对运行文档中库存 `status` 仅剩 schema legacy 说明与 SKILL.md 忽略规则。本次环境无可用 Python，`dev/validate_static.py`（含 schema 字段覆盖检查）未运行；新用例未交给独立 agent 执行。待办 F-06 的“3 天前写入、今天到期”验收依赖运行当天日期，静态 fixture 无法固定，改用已过期日期与过时 `status` 矛盾的场景代替。

### 关键进展

- 2026-10-11：用户要求修复待办 F-06；按 [DEC-027](DECISIONS.md#dec-027) 实施，约定范围完成后转为 implemented（验证缺口见上）。核对中发现 schema 黄金样例的库存条目缺少必填 `itemKey`，一并补上。

<a id="idea-030"></a>
## 采购提案记录时段与来源计划（待办 F-07）

- 编号：IDEA-030
- 状态：dropped
- 创建：2026-10-11
- 更新：2026-10-11
- 问题与预期结果：[待办 F-07](improvement-todo-2026-10-11.md#f-07) 认为每日搭配与周计划依赖的“当前时段”只存在于对话中，跨会话说“继续下一段”时 agent 只能猜日期，拟在 `shopping.json.confirmation` 记录时段起止日期、清单条目记录来源计划 `planId`。
- 范围／完成标准：放弃，不实施。
- 关联：[IDEA-023](#idea-023)；后续 [IDEA-031](#idea-031)。[DEC-004](DECISIONS.md#dec-004) 当时否决 segment 字段的判断继续有效。
- 实施：2026-10-11 曾在工作区实现（schema 两个新字段、周计划 4 条分支、两个用例），未提交；用户已撤回全部文件改动。当时草拟的 DEC-028 未保留，编号不复用。
- 验证与效果：无（未提交、未执行）。

### 关键进展

- 2026-10-11：实现后用户追问该场景是否常见。复核结论：时段多数情况可由当天日期、用户所说日期和采购节奏推出；必须依赖存储日期的只有“当前段未结束就提前规划下一段”“间隔多日仍要接续原段”等低频情况；需求来自文档推演而非真实失败，测试只能使用 2030 年日期规避运行日期，`planId` 无读取方。新增必填字段与分支与“减少规则”方向相反，放弃。

<a id="idea-031"></a>
## 按奥卡姆剃刀与 YAGNI 收敛运行契约（待办 V-01、V-02）

- 编号：IDEA-031
- 状态：implemented
- 创建：2026-10-11
- 更新：2026-10-11
- 问题与预期结果：普通增删改须先读 SKILL.md、schema.md、feedback_flow.md 约 6.4 万字符；规则随案例累加，反馈部分是无使用证据的文字状态机，规则越多遵守率越低。预期普通操作只读 SKILL.md，规划细节按需加载，删除没有失败案例支撑的机制，用户可见行为保持。
- 范围／完成标准：按 [DEC-029](DECISIONS.md#dec-029)。SKILL.md 重写为数据位置、9 条基本规则、各类操作要点、规划入口表、提醒表与格式；新建 references/planning.md 承载采购计划、每日搭配、食材咨询；删除 references/feedback_flow.md；schema.md 去掉 feedback.json 与 `confirmation`，定义数量 0 为“吃完”，画像简化并兼容旧字段；README、AGENTS.md 目录说明、quantity_benchmark.md 引用同步。F-01～F-06 的语义保留（食材池两种模式、过期保留并询问、只读不建文件、过期状态计算、宿主无关提醒、归类一致）。开发侧：fixture 去掉 feedback.json，`depleted_okra` 改为秋葵数量 0；依赖反馈机制的 `refill_decay`、`stock_change_deplete` 移入 historical_cases，新增 `eaten_up_keeps_zero`、`restock_after_eaten_up`；其余用例的 feedback 断言改为“不创建 feedback.json”，偏好用例改为断言 profile；schema 样例同步；历史文档中指向 feedback_flow.md 的 12 处链接改为提交 7460054 的固定链接。
- 关联：[DEC-029](DECISIONS.md#dec-029)；[待办 V-01、V-02](improvement-todo-2026-10-11.md#v-01)、[IDEA-023](#idea-023)；前序 [IDEA-009](#idea-009)、[IDEA-011](#idea-011)、[IDEA-018](#idea-018)、[IDEA-020](#idea-020)；[RQ-5](RESEARCH.md#rq-5) 暂停。
- 实施：[dd69d90](https://github.com/blizzardwj/pantry-man-skill/commit/dd69d90)。
- 验证与效果：2026-10-11 字符数：SKILL.md 33.6k → 7.8k，planning.md 4.7k，schema.md 19.8k → 6.8k，feedback_flow.md 11.2k → 删除；普通增删改的必读量约 6.4 万 → 7.8k 字符。Node 解析全部 fixture、用例与 schema 样例 JSON 通过；本地 Markdown 链接与锚点检查见本条关键进展。本次环境无可用 Python，`validate_static.py` 与 `run_golden.py` 未运行；简化前后没有执行基线，行为等价性未经验证。效果待用户实际使用观察，重点看：“吃完”后的数量 0 是否被正确写入并在采购计划中提示，过期询问、当天搭配只用库存是否仍被遵守。

### 关键进展

- 2026-10-11：用户认同“简单操作也要读大量说明”是本质问题，撤回 F-07，要求按奥卡姆剃刀与 YAGNI 收敛基本功能与反馈流程，反馈选方案 B，之后通过实际使用观察效果；按 DEC-029 实施，约定范围完成后转为 implemented（验证缺口见上）。
- 2026-10-11（验证补记）：基于提交 dd69d90（工作区另有仅文档改动），`validate_static.py` 由用户与 agent 各运行一次，FAIL 0、WARN 0，含传递式孤立引用检查与 53 个样例字段覆盖。`eaten_up_keeps_zero`、`restock_after_eaten_up` 的断言在未改动 fixture 上按预期 FAIL、在模拟正确结果上 PASS，说明 `quantity.value` 路径断言有效。这些是静态与断言层验证；skill 行为仍未经 agent 执行，效果待真实使用（V-07）与 A-03。
- 2026-10-11（验证补记）：首次由 agent 执行全部 19 个用例（Claude Code + Haiku），15 PASS；4 个失败中 2 个为 skill 缺陷（名称被翻译为英文）、2 个为用例问题，由 [IDEA-032](#idea-032) 修复后重跑 8/8 PASS。“吃完置 0”“补货写入新数量”“过期保留并询问”“当天搭配只用库存”“只读不建文件”的对应用例均通过。见 [执行报告](golden-run-2026-10-11.md)。

<a id="idea-032"></a>
## 首次 agent 执行暴露的问题修复：名称保留原话、用例断言修正

- 编号：IDEA-032
- 状态：implemented
- 创建：2026-10-11
- 更新：2026-10-11
- 问题与预期结果：首次由 agent 执行全部用例（[执行报告](golden-run-2026-10-11.md)），19 个中 4 个失败：用户说“牛奶”却写入 `milk`（2 例，skill 缺陷）；搭配回复正确说明“鲈鱼不计入今晚”却被 `not_contains` 判失败（断言过严）；`dry_good_no_soup` 用食材咨询去测原本发生在每日搭配的失真（用例对象错位）。预期修复后这 4 个用例稳定通过。
- 范围／完成标准：SKILL.md 基本规则 1 补“名称保留用户原话、不翻译”，schema.md 的 `name` 说明与示例改为中文原话；断言引擎新增正则谓词 `not_matches`；`pairing_meal_now_stock_only` 只检查食材／餐次行；`dry_good_no_soup` 改为搭配请求并断言食材行不含“汤”、做法种类 ≤2；新增 `dev/run_cases_claude.ps1` 作为 `claude -p` 执行脚本，结果目录 `dev/.golden_results/` 加入 .gitignore；dev/README.md 同步。
- 关联：[IDEA-023](#idea-023)（待办 A-03）、[IDEA-031](#idea-031)；[DEC-010](DECISIONS.md#dec-010)（dry_good_no_soup 的原始回归来源）；[DEC-029](DECISIONS.md#dec-029)（只为具体失败新增规则）。无新增决策或研究条目。
- 实施：[129b8ed](https://github.com/blizzardwj/pantry-man-skill/commit/129b8ed)。
- 验证与效果：2026-10-11 修复后用 Claude Code + Haiku 重跑 4 个用例各 2 次，8/8 PASS；`not_matches` 对真实回复 PASS、对构造的违规回复 FAIL。单一模型与执行者，其余 15 个用例未在修复后重跑；其他模型是否也会翻译名称未测试。

### 关键进展

- 2026-10-11：用户安装 Claude Code 并要求用 Haiku 执行每个用例；首轮 15/19，按失败原因区分 skill 缺陷与用例问题后修复，约定范围完成后转为 implemented（验证缺口见上）。

<a id="idea-033"></a>
## 照片输入：小票直接记录、识别类照片先确认（待办 A-04 扩展）

- 编号：IDEA-033
- 状态：implemented
- 创建：2026-10-12
- 更新：2026-10-12
- 问题与预期结果：用户提出除语音外也可拍照发给 agent。契约原先只按“用户所说”改数据，未定义照片含义；冰箱照片还有把未拍到的条目误删的风险。预期小票拍照即可记账，食材／冰箱照片先确认再写入且不误删。
- 范围／完成标准：按 [DEC-030](DECISIONS.md#dec-030)。SKILL.md 基本规则 1 与新增 Operations › Photos、description 提及照片；README 推荐宿主与“Say it or show it”示例；runner 支持用例 `attachments`（复制到临时 home 并写入委托提示词）；新增合成图片与两个用例，Haiku 各 3 次通过，并回归核心用例。
- 关联：[DEC-030](DECISIONS.md#dec-030)；[IDEA-023](#idea-023)（待办 A-04）；[验证方案](validation.md#core-cases)。
- 实施：[d9d3420](https://github.com/blizzardwj/pantry-man-skill/commit/d9d3420)。改动：SKILL.md、README.md；dev/run_golden.py（`attachments`）、dev/attachments/（合成小票、冰箱示意图）、golden case `photo_receipt_records_purchase`、`photo_fridge_confirm_first`；dev/validation.md、dev/README.md。
- 验证与效果：2026-10-12 Claude Code + Haiku：首轮小票 2/3、冰箱 0/3；修正规则措辞与用例提示后小票 3/3、冰箱 3/3，核心 7 用例回归 7/7，见[执行报告](golden-run-2026-10-11.md#addendum-2026-10-12-photo)。测试图为合成图，不代表真实照片的识别效果；真实照片待 L3 交互测试。

### 关键进展

- 2026-10-12：首轮两个失败均已定位：小票用例提示“刚才”与小票日期矛盾，且契约未说明小票是否算历史补记（agent 未勾选清单）；规则 1 改成“所说或清楚展示的”反被理解为可直接写入清楚的识别结果。改为“小票视同陈述、其他照片不视同”，并写明小票默认物品已到家、识别类即使被要求更新也先确认；重跑通过，约定范围完成后转为 implemented。
- 2026-10-12（验证补记）：新增用例 `photo_receipt_unreadable_no_guess`，使用用户以图像模型生成的带遮挡小票照片（单价与合计同时遮挡，排除推算路径），检验“看不清的不猜”；Haiku 3/3 PASS，见[执行报告](golden-run-2026-10-11.md#addendum-2026-10-12-photo)。无已知合计时 `stats.totalSpent` 在 null 与 0.0 间不一致，按 YAGNI 暂不加规则。

<a id="idea-034"></a>
## 回复跟随用户语言，支持英文用户（待办 V-05）

- 编号：IDEA-034
- 状态：implemented
- 创建：2026-10-12
- 更新：2026-10-12
- 问题与预期结果：用户决定面向英文用户投入。契约中的问句、标签与免责声明为固定中文，知识文件为中文，英文用户可能收到中文回复或中文免责声明。预期英文用户得到全英文回复，名称不被翻译，中文用户行为不变。
- 范围／完成标准：按 [待办 V-05](improvement-todo-2026-10-11.md#v-05) 与 [DEC-031](DECISIONS.md#dec-031)。SKILL.md 新增基本规则 10，规则 1 命名示例改为双向，规则 9 与定时提醒文案用用户语言；planning.md 开头注明中文标签为示例；README 说明支持中英文；新增英文 fixture 与 5 个 `en_*` 用例，并与旧契约对照。
- 关联：[DEC-031](DECISIONS.md#dec-031)；[IDEA-023](#idea-023)；[验证方案](validation.md#core-cases)。
- 实施：[9437f4c](https://github.com/blizzardwj/pantry-man-skill/commit/9437f4c)。改动：SKILL.md、references/planning.md、README.md；dev/fixtures/stocked_en、dev/fixtures/stocked_en_profile、dev/golden_cases/en_*.json；dev/validation.md。
- 验证与效果：2026-10-12 Claude Code + Haiku，新契约 en_* 用例 11/11 PASS（4 个各 2 次，免责声明用例 3 次）；旧契约对照免责声明用例 0/3、其余 4/4，见[执行报告](golden-run-2026-10-11.md#addendum-2026-10-12-language)。中文用例未在本次改动后重跑；数量基准对非中国饮食的适用性、单位换算未评估。

### 关键进展

- 2026-10-12：用户决定先投入面向英文用户；实施后对照旧契约，发现食材咨询路径在旧契约下回复中文或附中文免责声明，规则 10 有具体失败依据；约定范围完成后转为 implemented。
- 2026-10-12（验证补记）：9437f4c 全量回归 27/28；`en_add_keeps_name` 一次把 “milk” 写成 “牛奶”，重跑 4/4 通过，累计 7/8，记为间歇性问题，待 L3 观察，见[执行报告](golden-run-2026-10-11.md#addendum-2026-10-12-full)。

<a id="idea-035"></a>
## 补齐测试覆盖缺口，修订画像创建与月度统计规则

- 编号：IDEA-035
- 状态：implemented
- 创建：2026-10-12
- 更新：2026-10-12
- 问题与预期结果：2026-10-12 全面检查列出未被用例覆盖的行为：采购计划的补货提示、拿手菜保供、数量校验，确认后写入清单，过期条目回答后的处置，储备询问，首次画像确认；以及 totalSpent 在 null 与 0.0 间不一致。预期这些行为都有可重复执行的用例，暴露的契约问题得到修正。
- 范围／完成标准：新增 2 个 fixture、7 个用例并补强 2 个既有用例，Haiku 各至少 2 次通过；对暴露的问题按 [DEC-032](DECISIONS.md#dec-032) 修订 SKILL.md 与 schema.md，并回归核心用例。
- 关联：[DEC-032](DECISIONS.md#dec-032)；[IDEA-023](#idea-023)；[验证方案](validation.md#l2-writing)。
- 实施：本次工作区／尚未提交。改动：SKILL.md（Preferences 画像创建、Stats）、references/schema.md（totalSpent 定义与月份种子）；dev/fixtures/plan_base、dev/fixtures/fresh_only；dev/golden_cases 中 7 个新用例及 2 个补强用例。
- 验证与效果：见[执行报告](golden-run-2026-10-11.md#addendum-2026-10-12-coverage)：新用例最终全部通过（`profile_first_plan_summary` 经规则修订与断言放宽后 3/3），规则修订后回归 9/9。多轮场景以单轮提示模拟上一轮内容；定时提醒、单位换算、包装数量记法仍未覆盖。

### 关键进展

- 2026-10-12：用户要求先做快速整理再补测试覆盖；新用例暴露“空画像也要创建并确认”和 totalSpent 定义两处契约问题，按 DEC-029 原则仅针对具体失败修订；约定范围完成后转为 implemented。

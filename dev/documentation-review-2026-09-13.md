# 开发演进文档整理：验证与证据边界

- 日期：2026-09-13
- 对应工作：[IDEA-017](../IDEAS.md#idea-017)
- 决策：[DEC-016](../DECISIONS.md#dec-016)
- 基线：`4384a0f`；实现为本次工作区，尚未提交。提交时由 IDEA-017 补实施链接。
- 范围：IDEAS、RESEARCH、DECISIONS 的结构与追溯整理，以及 AGENTS 的维护规则。没有执行用户库存操作或反馈业务修复。

<a id="historical-evidence"></a>
## 历史实施与验证证据

本次根据仓库中的历史条目、Git 提交和用例文件建立链接。以下“未找到”只表示已查看的版本化文档中缺少可直接引用的执行结果，不证明历史上未执行过验证。原有试用描述保留在条目的“历史背景与讨论”中，不升级为本次验证结论。

| 条目 | 找到的证据 | 验证边界 |
|------|------------|----------|
| [IDEA-001](../IDEAS.md#idea-001)、[IDEA-002](../IDEAS.md#idea-002)、[IDEA-004](../IDEAS.md#idea-004)、[IDEA-007](../IDEAS.md#idea-007)、[IDEA-008](../IDEAS.md#idea-008) | 实现提交；部分相关初始化／食材池用例 | 未找到这些实现各自的完整执行报告；实际使用效果待观察 |
| [IDEA-006](../IDEAS.md#idea-006)、[IDEA-012](../IDEAS.md#idea-012) | 实现提交；做法与示例相关用例 | 用例定义不等于通过；未在本次运行 agent 生成效果评测 |
| [IDEA-009](../IDEAS.md#idea-009)、[IDEA-011](../IDEAS.md#idea-011) | 原始 schema／行为实现与迁移提交；库存变化、落点用例 | 不足以证明完整反馈生命周期正确；已知疑点集中列在 [RQ-5](../RESEARCH.md#rq-5)，本次未修复 |
| [IDEA-010](../IDEAS.md#idea-010) | 数量校验实现；历史回算描述见 [DEC-005](../DECISIONS.md#dec-005) | 未找到可复现该次回算的独立执行报告；不将历史描述写成本次 PASS |
| [IDEA-014](../IDEAS.md#idea-014) | 实现提交；[DEC-012](../DECISIONS.md#dec-012) 原文记载 static validation PASS | 未找到该次运行输出；长期咨询效果待观察 |
| [IDEA-015](../IDEAS.md#idea-015)、[IDEA-016](../IDEAS.md#idea-016) | schema、复用、泛化、升模板及采购保供实现提交 | 支持“实施已发生”，不证明实验性泛化或满意度改善已验证 |
| [IDEA-003](../IDEAS.md#idea-003)、[IDEA-005](../IDEAS.md#idea-005)、[IDEA-013](../IDEAS.md#idea-013) | 原问题与试用观察；[画像用例](golden_cases/profile_convergence.json) | 尚未实施对应改进或形成系统比较实验结论 |
| [DEC-006](../DECISIONS.md#dec-006)、[DEC-011](../DECISIONS.md#dec-011)、[DEC-015](../DECISIONS.md#dec-015) | 历史无单独想法条目；各决策已补提交和本报告入口 | 不追溯补造当时想法或验收结果；提醒适配、可选脚本能力和知识效果不在本次验证范围 |

所有历史来源日期沿用原记录，不据 Git 提交时间推定用户决定日期。原 RESEARCH 的外部文献本次未重新核验；保存原文不表示再次背书。

<a id="documentation-checks"></a>
## 本次文档验证

| 检查 | 结果 | 方法与覆盖 |
|------|------|------------|
| 编号、锚点与状态 | PASS | 17 个想法、4 个研究条目、16 个决策；显式锚点无重复，各条当前元数据恰有一个所属状态且取值有效；已完成想法有实施及验证入口 |
| 本地链接 | PASS | 临时只读检查解析 220 个本地 Markdown 链接，核对文件与目标锚点；模板代码块不参与计数 |
| 提交引用 | PASS | 41 个不同提交引用通过本地 `git cat-file -e <hash>^{commit}` 解析；未检查远程网页可达性 |
| 历史内容保留 | PASS | 与基线三文件逐条比较：除状态／日期元数据重组外，原正文完整保留；IDEA-005 的原研究主体移至 RESEARCH 的共享画像研究提案 |
| 变更范围 | PASS | 受版本控制的改动仅 AGENTS、IDEAS、RESEARCH、DECISIONS；新增本报告。SKILL、README、references 及开发期用例／工具均未改动 |
| L1 静态校验 | PASS，1 项已有警告 | 执行 `python3 dev/validate_static.py`，FAIL 0、WARN 1；frontmatter、4 个 reference 路径、跨 agent 路径与 63 个样例字段检查通过。警告是 SKILL 中既有的 4 处 `cron add` 占位示例，对应 DEC-006 |
| 差异格式 | PASS | `git diff --check` 无空白错误 |

文档检查于 2026-09-13 执行。编号、链接、历史保留检查使用一次性只读脚本，没有增加运行时依赖或文档维护专用测试框架。L1 为现有工具，未运行需要 agent 执行的 L2 黄金用例，也未把空跑断言当成业务验证。

本报告只证明相应检查覆盖的文档性质，不证明 feedback/reuse 的业务正确性；新文档结构能否持续降低维护遗漏仍待后续迭代观察。

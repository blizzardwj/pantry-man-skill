# Feedback 关联文档对齐复核 — 2026-09-30

范围：[IDEA-020](../IDEAS.md#idea-020)、[DEC-021](../DECISIONS.md#dec-021) 实施后的运行契约、演进文档和开发用例。本报告记录文档一致性检查，不把用例定义当成 agent 执行结果。

## 复核与修正

| 位置 | 发现 | 修正 |
|---|---|---|
| [Capture](../references/feedback_flow.md#capture-boundary)、[schema](../references/schema.md) | 边界判断与消费去向原先同列；“吃完”文字可能暗示来源一定是购买 | 独立标出是否属于 feedback、理由与后续用途；说明消耗不证明购买来源 |
| [RQ-5](../RESEARCH.md#rq-5)、[RQ-7](../RESEARCH.md#rq-7) | 当前摘要仍指向旧写前／恢复字段，历史草案中的“现行”链接已指向新版文件 | 更新当前摘要；将旧字段和候选方案明确标为历史，并链接对应旧提交与 DEC-021 |
| [IDEAS](../IDEAS.md)、[DECISIONS](../DECISIONS.md) | 已提交实现仍写“工作区／尚未提交”；耗尽决策的当前关系未指明恢复机制已被替代 | 补真实提交和双向后续链接，保留原事件日期与历史决策正文 |
| [开发用例](golden_cases/)与 [fixture](fixtures/depleted_okra/feedback.json) | 普通营养陈述被断言为个人偏好；当前样例仍携旧 `landings[]`／`clarificationAskedAt` | 将用例改为明确偏好；普通入库／历史购买断言不新增 feedback；当前样例去掉旧字段 |
| [2026-09-28 验证报告](feedback-refactor-review-2026-09-28.md)、[收敛建议](convergence-review-2026-09-28.md) | 历史设计易被读作当前规则 | 加历史标记和后续决策／实施链接，不改当时的测试结论 |

## 本次检查

- `dev/validate_static.py`：0 FAIL；既有 `cron add` 占位示例产生 1 WARN。
- 26 份开发 JSON（golden、schema probe、fixture、历史用例）解析通过。
- 14 份 Git 跟踪的 Markdown 文件：本地链接路径存在，显式锚点在各文件内唯一。
- `git diff --check` 通过；运行文件中 `landings[]` 等术语仅用于旧记录的保留／忽略说明，不再是新操作步骤。

这些是结构和文本一致性检查。新增或修订的 golden case 尚未交给独立 agent 执行，实际分类准确率与跨宿主行为仍待观察。

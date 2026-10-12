# dev/ — 设计文档与开发期验证（dev-only，不进 skill 分发）

pantry-man-skill 的**设计文档与开发期验证层**，与可选运行时脚本 `scripts/`（创建后进分发）分开：

| 目录 | 用途 | 进分发 |
|------|------|--------|
| `dev/`（本目录） | 架构方案、开发期验证与回归 | 否 |
| `scripts/` | 帮 agent 运行时把操作做对（校验） | 是 |

**验证方案（三种方式、何时运行、如何判定、结果记在哪里）见 [validation.md](validation.md)。**

## 内容

开发演进记录：

- `IDEAS.md` / `DECISIONS.md` / `RESEARCH.md` — 问题与实施进展／决策与有效性／研究进展（职责分工见根目录 AGENTS.md）
- `improvement-todo-YYYY-MM-DD.md` — 待办清单（范围与验收），完成状态由对应 IDEAS 条目维护
- `*-review-YYYY-MM-DD.md` — 各次复核报告，由 IDEAS 条目链接

验证（用法见 [validation.md](validation.md)）：

- `validation.md` — 完整验证方案：L1 静态校验、L2 用例执行、L3 交互测试
- `validate_static.py` — L1 静态校验（零 LLM）
- `run_golden.py` — L2 runner：prepare／assert／run／run-all
- `run_cases_claude.ps1` — L2 自动执行：`claude -p` 作为执行者批量运行用例
- `lib/assert_engine.py` — 断言引擎（纯函数，零 LLM）
- `golden_cases/` — 用例定义（`{id, prompt, fixture, assert}`，与执行者无关）
- `historical_cases/` — 已被新规则替代的旧用例，只供追溯，不参与运行
- `fixtures/` — 用例的初始数据（每个 fixture 一个目录）
- `schema_probe/` — schema 黄金样例，供 L1 字段覆盖检查
- `golden-run-YYYY-MM-DD.md` — L2 执行报告，由 IDEAS 条目链接
- `usage-log.md` — L3 日常使用记录（首次记录时创建）
- `.golden_results/` — L2 自动执行的日志（不入库）

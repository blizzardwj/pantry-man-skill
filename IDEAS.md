# IDEAS — 想法池

> 未实施的想法都在这里。状态流转：`idea` → `planned` → `implemented` / `dropped`。
> 被丢弃的想法**不要删除**，标 `dropped` 并写原因——那是最有价值的记录。

<!-- 模板：
## [想法标题]
- 状态: idea / planned / implemented / dropped
- 日期: YYYY-MM-DD
- 动机: 为什么有这个想法
- 评估: 成本 / 收益 / 风险
- 备注: 相关讨论或链接
-->

## First-Run 初始化
- 状态: **implemented** (commit 32c8c0f)
- 日期: 2026-07-31
- 动机: 首次使用 skill 时数据文件不存在，agent 操作会冷启动失败
- 评估: 成本低（14 行指令），解决最严重的 UX 问题；跨 agent 通用，不破坏兼容性
- 备注: 用 `[AGENT_HOME]` 保持 agent 无关；已存在时静默跳过

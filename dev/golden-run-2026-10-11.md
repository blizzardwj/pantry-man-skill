# Golden case 首次 agent 执行 — 2026-10-11

- 对应条目：[IDEA-032](IDEAS.md#idea-032)（失败修复）、[IDEA-023](IDEAS.md#idea-023)（待办 A-03）
- 基线：提交 `dd69d90`（DEC-029 收敛后的契约）；工作区另有仅文档改动。第二轮在本报告所述修复之后执行，修复为本次工作区／尚未提交。
- 执行者：Claude Code CLI 2.1.296，`claude -p --model haiku`，Windows 11；断言与 runner 使用 Python 3.14.7（conda）。
- 方式：每个用例由 `run_golden.py prepare` 建立临时 agent home，agent 在该 home 内运行，仓库仅以 `--add-dir` 供读取 SKILL.md 与 references；允许工具 Read／Write／Edit／Glob／Grep，`acceptEdits`。结束后 `run_golden.py assert` 判定。每轮后检查仓库 `git status`，均无 agent 写入。执行脚本见 [run_cases_claude.ps1](run_cases_claude.ps1)（首轮由同内容的临时脚本执行）。

## 第一轮：全部 19 个用例，各执行一次

结果：**15 PASS / 4 FAIL**。

| 用例 | 结果 | 耗时 |
|---|---|---|
| add_inventory | FAIL | 30s |
| dry_good_no_soup | FAIL | 23s |
| eaten_up_keeps_zero | PASS | 41s |
| expired_discarded | PASS | 18s |
| expired_kept_on_view | PASS | 15s |
| explicit_breakfast_preference | PASS | 18s |
| first_run_add_initializes | FAIL | 20s |
| first_run_consult_no_init | PASS | 36s |
| first_run_view_no_init | PASS | 15s |
| pairing_meal_now_empty_list | PASS | 26s |
| pairing_meal_now_stock_only | FAIL | 27s |
| pairing_minimal_methods | PASS | 22s |
| pairing_segment_pending_marked | PASS | 50s |
| pool_hard_constraint | PASS | 27s |
| profile_convergence | PASS | 20s |
| purchase_history | PASS | 19s |
| purchase_without_feedback | PASS | 26s |
| restock_after_eaten_up | PASS | 25s |
| stale_status_ignored | PASS | 15s |

### 失败分析

| 用例 | 观察 | 归类 | 处理 |
|---|---|---|---|
| add_inventory、first_run_add_initializes | 用户说“牛奶”，写入 `name: "milk"`。schema 示例名均为英文（`milk`、`tomato`），且无“保留用户原话”的规则 | skill 缺陷 | SKILL.md 基本规则 1 补“名称保留用户原话、不翻译”；schema 示例名改为中文 |
| pairing_meal_now_stock_only | 回复正确地只用库存，并说明“购物清单上的鲈鱼不计入今晚”；`not_contains 鲈鱼` 把提及误判为使用 | 断言过严 | 新增文本谓词 `not_matches`（正则），只检查以 食材／早餐／午餐／晚餐 开头的行 |
| dry_good_no_soup | 提问“香菇怎么吃”触发食材咨询，回答中提到煲汤、泡发水作高汤，属于合理内容。原回归（[DEC-010](DECISIONS.md#dec-010)）发生在每日搭配：给单味干香菇配“香菇煮汤” | 用例对象错位 | 改为搭配请求“今晚用家里的东西做点什么吃”，断言食材行不含“汤”、做法种类 ≤2 |

## 第二轮：修复后重跑 4 个用例，各执行两次

结果：**8／8 PASS**（add_inventory、first_run_add_initializes、dry_good_no_soup、pairing_meal_now_stock_only 各 2 次）。另用仓库内脚本跑 first_run_view_no_init 一次作脚本冒烟，PASS。

断言自测：新 `not_matches` 对第一轮的真实回复 PASS，对把鲈鱼写进食材行的构造回复 FAIL。

## 证据边界

- 单一执行者与模型（Claude Code + Haiku），第一轮通过的 15 个用例只跑一次，未测稳定性；它们在修复前的契约上执行，修复只新增一条命名规则与 schema 示例，未重跑。
- 文本断言是启发式（子串、正则、做法动词计数），只能捕捉已知失真形态，不评价回复质量。
- 用例未覆盖：采购计划中对“吃完”条目的补货提示、拿手菜保供、数量校验报告、过期条目回答后的处置、冷启动储备询问。
- 这是开发期执行证据，不代表真实使用效果；真实使用观察见待办 [V-07](improvement-todo-2026-10-11.md#v-07)。

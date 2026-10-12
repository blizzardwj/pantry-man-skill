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

<a id="addendum-2026-10-12"></a>
## 补充（2026-10-12）：语音式多项操作用例

- 背景：待办 A-04 在 README 中加入“一句话说出多项变化”的语音示例；按 A-05“不展示未实现能力”的要求，先以用例验证。
- 用例：`voice_multi_op`，指令“买了两盒牛奶和一把菠菜，鸡蛋吃完了，过期的酸奶扔了”；fixture `voice_multi_op`（冷藏有鸡蛋 6 个、过期酸奶 1 盒，清单有牛奶 2 盒）。断言：牛奶 2 入库且清单勾选、菠菜入库、鸡蛋数量 0、酸奶删除、不创建 feedback.json。
- 执行：Claude Code 2.1.296 + Haiku，`dev/run_cases_claude.ps1`，基线提交 `129b8ed` 加 README 改动，连续 3 次：**3/3 PASS**，平均约 30s；仓库无 agent 写入。
- 观察：回复逐项列出改动；购买同时写入 `history/2026-10.json`，无价格时 `totalSpent` 记 0.0 并说明只是已知金额合计（与基本规则 1 一致）。History 未断言（文件名依赖运行月份）。
- 局限：单一模型与执行者；未测语音转写错误（同音字、漏词）对解析的影响。

<a id="addendum-2026-10-12-photo"></a>
## 补充（2026-10-12）：照片输入用例

- 背景：A-04 增加拍照输入（[DEC-030](DECISIONS.md#dec-030)）。runner 新增用例字段 `attachments`；测试图为合成图：渲染的盒马小票（2026-10-10，伊利纯牛奶250ml×12 ¥39.90、菠菜 500g ¥4.50、合计 ¥44.40）与带文字标签的冰箱示意图（鸡蛋×6、牛奶 2 盒；库存中的苹果、黄瓜未出现）。
- 用例：`photo_receipt_records_purchase`（牛奶清单项勾选、菠菜入库、`history/2026-10.json` 记 10-10 合计 44.4）；`photo_fridge_confirm_first`（不写入牛奶，苹果 3、黄瓜 2、鸡蛋 6 不变，回复列出牛奶并请求确认）。
- 第一轮（Haiku，各 3 次）：小票 2/3，冰箱 0/3。小票失败一次：提示“刚才的小票”与小票日期 10-10 矛盾，agent 按历史补记处理未勾选清单。冰箱三次均直接写入牛奶：当时规则 1 为“所说或清楚展示的”，标签清晰即被视为可写入；“看不到不删除”三次均遵守。
- 修复：规则 1 改为“小票视同陈述，其他照片不视同”；Photos 写明小票默认物品已到家并勾选清单、识别类即使被要求更新也先确认；小票用例提示改为中性“这是买菜的小票”。
- 第二轮（各 3 次）：小票 3/3，冰箱 3/3；冰箱回复列出识别结果、标注估计并说明“确认前未改动”。规则 1 改动后核心 7 用例回归 7/7。仓库均无 agent 写入。
- 局限：合成图只检验规则执行，不代表真实照片（遮挡、反光、手写小票）的识别效果；未测食材照片单独用例（与冰箱照片同一规则）。
- 补充用例 `photo_receipt_unreadable_no_guess`（2026-10-12）：图像模型生成的小票照片 `receipt_hema_20261010_occluded.jpg`，菠菜单价与合计被咖啡渍完全遮挡，其余文字经人工核对与规格一致。断言：历史记录无 `total`、菠菜入库、清单牛奶勾选、回复说明看不清。Haiku 3 次：**3/3 PASS**；三次均未写菠菜价格、未推算或编造合计，看得清的牛奶 39.90、鸡蛋 12.80 照常记录，回复请用户补充数字。观察：无已知合计时 `stats.totalSpent` 两次为 `null`、一次为 `0.0`（按 schema“已知金额之和”定义 0.0 合规）；牛奶数量两次记 1 件、一次记 12 盒，契约未规定，暂不处理。
- 同日：为控制仓库体积，该图由 PNG（2.4 MB）转为 JPEG（质量 82，原分辨率 1448×1086，约 232 KB），人工核对文字与遮挡不变；用例改用 `.jpg` 后 Haiku 重跑 2 次，2/2 PASS。

<a id="addendum-2026-10-12-language"></a>
## 补充（2026-10-12）：英文用户（V-05）

- 新增 fixture `stocked_en`（英文名称，含过期酸奶，清单有 salmon）、`stocked_en_profile`（另含糖尿病画像），用例 `en_add_keeps_name`、`en_eaten_up`、`en_view_expired`、`en_meal_tonight`、`en_disclaimer_language`；断言回复不含中文字符（`not_matches [一-鿿]`，经注入中文标签的构造回复验证会 FAIL）且名称不翻译。委托提示词为中文，相当于中文宿主中的英文用户，比实际使用更严格。
- 新契约（规则 10 等）：前 4 个用例各 2 次 8/8 PASS；`en_disclaimer_language` 3/3 PASS。
- 旧契约对照（用 `git archive HEAD` 生成的副本运行，不改动工作区）：前 4 个用例 4/4 PASS；`en_disclaimer_language` **0/3**——两次整篇中文（沿用 ingredient_knowledge.md 的中文标题），一次英文正文但逐字附中文免责声明。结论：语言问题集中在中文知识文件与固定中文文案的路径，规则 10 有具体失败依据。
- 局限：仅 Haiku；未测中英混用的用户、单位换算。

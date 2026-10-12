# 验证方案（Validation）

pantry-man-skill 的完整验证方案：三种方式、何时运行、如何判定、结果记在哪里。工具均为开发期使用，不进 skill 分发。

<a id="overview"></a>
## 三种方式

| 方式 | 是否需要 agent | 回答的问题 | 判定 | 成本 |
|---|---|---|---|---|
| [L1 静态校验](#l1) | 否 | 文档本身是否合规：引用路径、宿主专属写法、schema 字段覆盖 | `validate_static.py`，确定性 | 秒级 |
| [L2 用例执行](#l2) | 是（命令行启动 agent 执行委托提示词） | 某模型能否执行 skill 的规则 | `run_golden.py assert`，确定性 | 每用例约 15–50 秒及模型额度 |
| [L3 交互测试](#l3) | 是（用户在宿主中直接对话） | 真实宿主、模型和说法下是否被调起并做对、是否省事 | 快照对比 + 检查清单 + 使用记录 | 人工 |

三者互补：L1 查不出 agent 行为（如把“牛奶”写成 `milk`）；L2 可重复、可自动判定，但不测宿主加载 skill、语音转写与真实说法；L3 覆盖这些环节，但难以重复。L3 发现的问题应尽量转成 L2 用例（见[从问题到回归用例](#from-failure-to-case)）。

<a id="when"></a>
## 何时运行什么

| 场景 | L1 | L2 | L3 |
|---|---|---|---|
| 只改 dev/ 文档或记录 | ✅ | — | — |
| 改 SKILL.md、references/ 或 schema | ✅ | 受影响用例 + [核心用例](#core-cases) | — |
| 新增或修改用例、断言、runner | ✅ | 新用例在当前版本 PASS；能捕捉问题的用例先在问题版本上 FAIL | — |
| 发布或推广前 | ✅ | 全部用例；至少两个模型，或同一模型多次 | 一、二 |
| 换宿主或模型（如 Hermes + deepseek-flash） | — | — | 一、二 |
| 日常使用（[V-07](improvement-todo-2026-10-11.md#v-07)） | — | — | 三 |

<a id="principles"></a>
## 共同原则

- 以数据最终状态为准，不以 agent 的自我报告为准（L2 中 agent 均报告“完成”，却写入了 `milk`）。
- 判定尽量确定性：断言只针对可客观判断的事实（数量、文件是否存在、某行是否出现某词），不评文案好坏。
- 每轮记录日期、宿主、模型、skill 对应提交（`git log --oneline -1`）。不同模型的结果不能互相代替。
- 验证工具使用纯 Python 标准库，零依赖；Windows 控制台为 GBK 时用 `python -X utf8` 运行（`-I` 会忽略 `PYTHONIOENCODING`）。

---

<a id="l1"></a>
## L1 静态校验（不用 agent）

```bash
python dev/validate_static.py                                             # 含黄金样例字段覆盖（CI 可用）
python dev/validate_static.py --data [AGENT_HOME]/pantry/data/pantry.json # 附真实数据字段覆盖
```

检查项：

1. SKILL.md frontmatter：`name: pantry-man` 与非空 `description`。
2. SKILL.md 引用的 `references/*.md` 均存在。
3. references/ 中没有孤立文件（从 SKILL.md 出发、沿 references 之间的链接可达）。
4. 无硬编码 agent 路径（`~/.hermes` 等）、无宿主专属命令（`cron add`、`HEARTBEAT.md`）、数据路径均以 `[AGENT_HOME]/` 开头。
5. [schema_probe/](schema_probe/) 中所有字段名都在 schema.md 中出现；`--data` 对真实数据做同样检查，可发现 agent 自造的字段。

结果：`FAIL: 0` 才算通过；WARN 需说明原因或消除。

---

<a id="l2"></a>
## L2 用例执行（命令行启动 agent）

<a id="l2-flow"></a>
### 流程

```
golden_cases/<id>.json + fixtures/<name>/
  ① prepare  建临时 agent home，复制 fixture 到 pantry/data/，生成委托提示词
  ② execute  agent 在临时 home 内读 SKILL.md 并执行用户指令（数据目录被覆盖为临时目录）
  ③ assert   不调用模型，对 pantry/data/*.json 与 response.txt 的最终状态做确定性判定
  ④ 汇总     PASS／FAIL、各断言结果、agent 报告与临时 home 路径（保留，便于排查）
```

委托提示词要求 agent 把 `[AGENT_HOME]/pantry/data` 一律替换为临时目录、先读仓库中的 SKILL.md；断言检查 `response.txt` 时，还要求把完整回复写入 `<home>/response.txt`。因此 L2 测“规则能否被执行”，不测 skill 能否被宿主自动调起（那是 [L3 二](#l3-trigger)）。

<a id="l2-run"></a>
### 运行

自动（Claude Code CLI 作为执行者，PowerShell）：

```powershell
pwsh dev/run_cases_claude.ps1                                         # 全部用例，默认 haiku
pwsh dev/run_cases_claude.ps1 -Ids eaten_up_keeps_zero,voice_multi_op -Model sonnet
# 可选参数：-Python <python 路径> -Claude <claude 路径>
# 结果：dev/.golden_results/summary.tsv 及各用例 <id>.agent.txt／<id>.assert.txt（不入库）
```

脚本让 agent 在临时 home 内运行，仓库只以 `--add-dir` 供读取，工具限 Read／Write／Edit／Glob／Grep（无 Bash），`acceptEdits` 自动批准写入。`acceptEdits` 在 add-dir 中同样允许写，隔离并非绝对：每轮后检查仓库 `git status`，确认无 agent 写入。

手动（任意执行者，如 Hermes、`codex exec` 或人工）：

```bash
python dev/run_golden.py prepare <case_id>             # 输出 {home, data_dir, delegation_prompt}
#   把 delegation_prompt 交给执行者
python dev/run_golden.py assert <case_id> --home <home>
python dev/run_golden.py run <case_id>                 # prepare + 暂停等待人工执行 + assert
python dev/run_golden.py run-all [--no-wait]           # 全部用例；--no-wait 跳过暂停，直接断言当前状态
```

<a id="core-cases"></a>
### 核心用例

| 用例 | 覆盖的规则 |
|---|---|
| `add_inventory` | 名称保留用户原话；不建多余文件 |
| `eaten_up_keeps_zero` | 吃完 → 数量 0，条目保留 |
| `restock_after_eaten_up` | 补货写入新数量，不重复建条目 |
| `expired_kept_on_view` | 过期保留并询问处置 |
| `pairing_meal_now_stock_only` | 当天搭配只用库存，待买不算 |
| `first_run_view_no_init` | 只读请求不建文件 |
| `voice_multi_op` | 一句话多项操作：买了、吃完、扔了 |
| `photo_receipt_records_purchase` | 小票照片直接记为购买：入库、勾选清单、按小票日期与金额记历史 |
| `photo_receipt_unreadable_no_guess` | 小票部分被遮挡：看不清的单价与合计不写、不推算，看得清的照常记录，并告知用户 |
| `photo_fridge_confirm_first` | 冰箱照片先列识别结果并请求确认，确认前不写入；看不到的条目不删除、不置 0 |

全部用例见 [golden_cases/](golden_cases/)；已被新规则替代的旧用例在 [historical_cases/](historical_cases/)，只供追溯，不参与运行。

<a id="l2-case-format"></a>
### 用例定义

```json
{
  "id": "explicit_breakfast_preference",
  "prompt": "我喜欢早餐吃洋葱和自制酸奶，以后搭配早餐时可以多考虑它们",
  "fixture": "empty",
  "assert": {
    "profile.json": [{"path": "preferences.prefer", "count_gte": 1}],
    "feedback.json": [{"exists": false}]
  }
}
```

- `fixture`：`dev/fixtures/<name>/` 的初始数据，复制到临时 home 的 `pantry/data/`；`null` 表示尚无数据，不创建 `pantry/data/`（首次使用场景）。
- `attachments`（可选）：用户随消息发来的文件（如照片），取自 [attachments/](attachments/)；prepare 复制到临时 home 的 `attachments/`，并在委托提示词中列出路径，要求 agent 先查看。
- `assert` 的键是目标文件：`pantry/data/` 下的 `*.json`（结构化断言），或 home 根目录的 `response.txt`（agent 回复文本）。

<a id="l2-predicates"></a>
### 断言谓词

文件级（任意目标文件）：
- `exists` — `true`／`false`，文件存在或不存在（如只读请求不应创建数据文件）。

结构化（`*.json`，作用于点号路径 `path`）：
- `contains` / `not_contains` — 数组内匹配（对象数组按 `name` 字段；字符串数组直接匹配）。
- `record_exists` — 数组内存在元素满足所有 `字段路径 == 值`，字段路径可用点号（如 `"quantity.value": 0`）。
- `field_equals` — 路径解析值相等。
- `count_gte` / `count_equals` — 数组长度。

文本（`*.txt`）：
- `contains` / `not_contains` — 子串检查。
- `contains_any` — 至少出现其中一个子串（如回答用到了任一库存食材）。
- `not_matches` — 正则不匹配；用于只检查特定行，如 `(食材|早餐|午餐|晚餐)[^\n]*鲈鱼` 允许在说明中提及“鲈鱼不计入今晚”。
- `max_method_types` — 做法中出现的烹饪动词种类数 ≤ max（如 `{"methods": ["焯","蒸","煮","烙","拌","炒","炖","煎","炸","烤"], "max": 3}`）。

<a id="l2-writing"></a>
### 编写用例

- 图片附件：仓库内的测试图片均为合成图（代码渲染的小票与冰箱示意图，以及图像模型生成的带遮挡小票照片），用于检验规则执行，不代表真实照片的识别效果；真实照片在 L3 中验证。生成后须核对：看得清的文字与断言一致，被遮挡处透不出可辨认的内容。
- 负面用例要遮住所有可推出答案的线索：例如只遮单价、留着合计，agent 可以合理推算，就测不到“不猜”。
- 日期固定：过期用已过去的固定日期；需要“未来”的场景用远期日期；不断言依赖运行日期的内容（如 `history/<当月>.json` 的文件名）。
- 文本断言只捕捉已知的失真形态；避免把“提及”误判为“使用”，必要时用 `not_matches` 限定到食材行。
- 一个用例对应一条规则或一个真实失败；用户可见的承诺（如 README 示例）应有对应用例。
- 新用例应先确认能捕捉问题：在问题版本或未改动的 fixture 上 FAIL，在正确结果上 PASS。

<a id="l2-triage"></a>
### 失败判断

先打开临时 home 中的实际产物，再对照用例本意：

| 归类 | 判断 | 处理 |
|---|---|---|
| skill 缺陷 | 产物违反 skill 意图 | 修改 SKILL.md／references（只针对该失败） |
| 断言过严 | 产物正确，断言误判 | 修正断言 |
| 用例对象错位 | 用例测错了功能或场景 | 重写用例 |

修复后重跑失败用例，最好多次，观察稳定性。

<a id="l2-record"></a>
### 记录

每轮写一份 `golden-run-YYYY-MM-DD.md`（执行者、模型、版本、逐用例结果、失败分析、证据边界），由 IDEAS 条目链接。示例：[golden-run-2026-10-11.md](golden-run-2026-10-11.md)。

---

<a id="l3"></a>
## L3 交互测试（用户直接与 agent 对话）

<a id="l3-prepare"></a>
### 准备

- skill 已安装在宿主中，并与仓库当前版本一致；skill 有改动后先同步再测。
- 确认宿主的数据目录 `[AGENT_HOME]/pantry/data`，例如 Windows 上的 Hermes 为 `%LOCALAPPDATA%\hermes\pantry\data`。

<a id="snapshot"></a>
### 快照对比（L3 通用工具）

```powershell
$data = "$env:LOCALAPPDATA\hermes\pantry\data"          # 换成所用宿主的数据目录
$snap = "$env:TEMP\pantry_snap_$(Get-Date -Format yyyyMMdd_HHmm)"
if (Test-Path $data) { Copy-Item $data $snap -Recurse }   # 对话前
# …… 在宿主中对话 ……
git diff --no-index $snap $data                          # 对话后：逐行查看改动
python dev\validate_static.py --data "$data\pantry.json" # 是否出现 schema 未定义的字段
```

数据目录对话前不存在时，对话后用 `Test-Path $data` 判断是否被创建。

<a id="l3-replay"></a>
### 一、在宿主中复现 L2 用例

判断“该宿主 + 该模型能否执行规则”。prepare 与 assert 不变，执行者换成宿主中的一次新会话：

```powershell
$id = "eaten_up_keeps_zero"
$p = python dev\run_golden.py prepare $id | ConvertFrom-Json
$p.delegation_prompt | Set-Clipboard     # 复制委托提示词
# → 在宿主中选定模型、开新会话、粘贴发送，等待完成
python dev\run_golden.py assert $id --home $p.home
```

不碰真实数据，也不测试触发；宿主需能读取仓库路径、写入临时目录。先跑[核心用例](#core-cases)。失败时用 L2 基线模型跑同一用例对照：

- 基线通过、宿主失败：先排除宿主因素（提示词是否完整送达、是否允许写临时目录），再判断为模型执行问题。
- 两者都失败：按 [L2 失败判断](#l2-triage) 处理。

<a id="l3-trigger"></a>
### 二、触发测试

每句话开一个新会话，不提 skill 名，前后做[快照对比](#snapshot)：

| 说法 | 预期 |
|---|---|
| “冰箱里有什么” | 调用 skill 并列出库存；只读，数据无变化（无数据时不创建目录） |
| “苹果吃完了” | 调用 skill；苹果 `quantity.value` 变为 0 |
| “列个采购清单”／“今晚吃什么” | 调用规划功能；采购清单在确认前不写入 |
| “海带怎么炖好吃”（与自家库存无关） | 不调用 skill，或调用但不创建、不修改任何数据 |

是否调用：看回复是否体现 skill 的规则（按库存回答、提到“已吃完”等），或宿主是否显示加载了该 skill。

<a id="l3-daily"></a>
### 三、日常使用观察（真实数据）

每次使用前后做[快照对比](#snapshot)，按清单核对 diff：

1. “X 吃完了” → 该条目 `quantity.value` 为 0，未被删除；下次采购计划提示“上次吃完，可补”。
2. “今晚吃什么” → 回复不含待买或已吃完的食材。
3. 查看库存 → 过期条目仍在、询问一次处置，并按回答处理（吃完 → 0；扔了 → 删除；还在 → 保留）。
4. “这周买什么” → 只规划下一趟采购，确认后才写入 `shopping.json`。
5. 语音输入 → 多项操作逐项生效；`name` 为原话，没有错字或翻译。
6. 照片 → 小票：直接入库、勾选清单、历史中的日期和金额与小票一致；食材或冰箱照片：先列识别结果并请求确认，确认前 diff 为空，看不到的条目未被删除或置 0。

<a id="l3-record"></a>
### 记录与归因

问题记入 `dev/usage-log.md`（首次记录时创建），每轮注明宿主、模型、skill 提交，每个问题一行：

| 日期 | 原话 | 预期 | 实际（来自 diff） | 归因 |
|---|---|---|---|---|
| 示例 | 买了半斤虾仁 | 冷冻区新增虾仁 | `name: "虾人"` | 输入遗漏（转写错误） |

| 归因 | 含义 | 处理方向 |
|---|---|---|
| 输入遗漏 | 转写错误、用户没说或没报告 | 宿主或输入环节；考虑“拿不准时确认”而不是加业务规则 |
| 解析错误 | 说清楚了但理解错（把扔了当吃完） | 检查对应基本规则是否表达清楚 |
| 状态未更新 | 理解对了但文件没改或改错 | 检查操作说明与 schema |
| 规划规则错误 | 数据正确但计划或搭配不对 | 检查 references/planning.md |

除问题外，也记下实际采用了哪些建议、是否愿意继续使用及原因，作为 V-07 的效果证据。

---

<a id="from-failure-to-case"></a>
## 从问题到回归用例

1. 能用固定数据复现的问题（来自 L3 或 L2），整理成 golden case：把出问题前的数据精简为 fixture，原话作为 `prompt`，预期写成断言。
2. 用 L2 跑一次，确认用例在当前版本上 FAIL。
3. 只针对这个具体失败修改 skill（[DEC-029](DECISIONS.md#dec-029)），修复后 L1、L2 通过，必要时 L3 复测。
4. 在 IDEAS 中记录问题、修复与复测结果，并链接执行报告或使用记录。

依赖运行日期的问题（如“今天到期”）不适合做成固定 fixture，保留在使用记录中。

<a id="records"></a>
## 结果记录位置

| 方式 | 记录 | 链接到 |
|---|---|---|
| L1 | 运行结果写入对应 IDEAS 条目的“验证与效果”或关键进展 | 实施该改动的 IDEA |
| L2 | `golden-run-YYYY-MM-DD.md` | 对应 IDEA；待办 A-03 由 IDEA-023 维护 |
| L3 | `usage-log.md` | IDEA-023（V-07）；转成用例的问题另建 IDEA |

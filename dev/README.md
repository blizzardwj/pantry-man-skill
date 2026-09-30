# dev/ — 设计文档与开发期验证（dev-only，不进 skill 分发）

pantry-man-skill 的**设计文档与开发期验证层**，与可选运行时脚本 `scripts/`（创建后进分发）分开：

| 目录 | 用途 | 进分发 |
|------|------|--------|
| `dev/`（本目录） | 架构方案、开发期验证与回归 | 否 |
| `scripts/` | 帮 agent 运行时把操作做对（校验） | 是 |

## 内容

- `validate_static.py` — L1 静态校验（零 LLM），自动化 AGENTS.md Verification Checklist
- `run_golden.py` — L2 runner：setup fixture → executor 跑 prompt → 断言数据状态
- `lib/assert_engine.py` — 断言引擎（纯函数，零 LLM）
- `fixtures/` — 初始数据快照（每个 fixture 一个目录，含 pantry.json 等）
- `golden_cases/` — 用例定义（`{id, prompt, fixture, assert}`，agent 无关）
- `historical_cases/` — 已被新运行规则替代的旧用例定义，只供追溯，不参与 `run-all`
- `schema_probe/` — schema 黄金样例（写满全部字段，供 L1 字段覆盖检查，CI 可用）

## 用法

```bash
# L1 静态校验
python3 dev/validate_static.py                                          # 含黄金样例字段覆盖（CI 安全）
python3 dev/validate_static.py --data [AGENT_HOME]/pantry/data/pantry.json # 附真实数据字段覆盖

# L2 黄金用例
python3 dev/run_golden.py prepare <case_id>   # setup fixture，输出 {home, data_dir, delegation_prompt}
#   把 delegation_prompt 交给执行者（delegate_task / claude -p / codex exec）
python3 dev/run_golden.py assert <case_id> --home <home>   # 对执行结果断言
python3 dev/run_golden.py run <case_id>       # manual：prepare + 暂停 + assert
python3 dev/run_golden.py run-all             # 全部用例（manual）；--no-wait 跳过暂停，断言当前状态
```

## Golden case 定义

每个用例是 `dev/golden_cases/*.json`：

```json
{
  "id": "explicit_breakfast_preference",
  "prompt": "我喜欢早餐吃洋葱和自制酸奶，以后搭配早餐时可以多考虑它们",
  "fixture": "empty",
  "assert": {
    "feedback.json": [
      {"path": "records", "record_exists": {"type": "preference-correction"}}
    ]
  }
}
```

- `fixture`：`dev/fixtures/<name>/` 里的初始数据，被复制到临时 agent home 的 `pantry/data/`
- `assert` 目标文件：`*.json`（结构化断言）或 `response.txt`（agent 回复文本，manual 模式下手动放置）

### 断言谓词

结构化（`*.json`，作用于点号路径 `path`）：
- `contains` / `not_contains` — 数组内匹配（dict 数组按 `name` 字段；字符串数组直接匹配）
- `record_exists` — 数组内存在元素满足所有 `字段路径 == 值`
- `field_equals` — 路径解析值相等
- `count_gte` / `count_equals` — 数组长度

文本（`*.txt`）：
- `contains` / `not_contains` — 子串检查（负向词表，如 `not_contains ["汤"]` 抓「香菇煮汤」失真）
- `max_method_types` — 统计做法中烹饪动词种类数 ≤ max（如 `{"methods": ["焯","蒸","煮","烙","拌","炒","炖","煎","炸","烤"], "max": 3}`，抓「每食材一动作」排比）

## 原则

- 验证工具使用纯 Python 标准库，零依赖
- 断言只针对数据文件最终状态（objective ground truth），不评文案好坏
- executor 是薄接口：现在 manual，后续接 Hermes delegate / `claude -p` / `codex exec`
- 不进入 skill 分发

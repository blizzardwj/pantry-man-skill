# dev/ — 开发期验证（dev-only，不进 skill 分发）

pantry-man-skill 的**开发期验证层**，与运行时脚本 `scripts/`（进分发）正交：

| 目录 | 用途 | 进分发 |
|------|------|--------|
| `dev/`（本目录） | 测 skill 本身对不对（回归） | 否 |
| `scripts/` | 帮 agent 运行时把操作做对（校验） | 是 |

## 内容

- `validate_static.py` — L1 静态校验（零 LLM），自动化 AGENTS.md Verification Checklist
- `run_golden.py` — L2 runner：setup fixture → executor 跑 prompt → 断言数据状态
- `lib/assert_engine.py` — 断言引擎（纯函数，零 LLM）
- `fixtures/` — 初始数据快照（每个 fixture 一个目录，含 pantry.json 等）
- `golden_cases/` — 用例定义（`{id, prompt, fixture, assert}`，agent 无关）

## 用法

```bash
# L1 静态校验
python3 dev/validate_static.py
python3 dev/validate_static.py --data ~/.hermes/pantry/data/pantry.json   # 附加 schema 字段覆盖

# L2 黄金用例（manual executor）
python3 dev/run_golden.py --all                # 每个用例 setup 后暂停，手动跑 agent 再回车断言
python3 dev/run_golden.py --case add_inventory
python3 dev/run_golden.py --all --no-wait      # 跳过暂停，断言当前状态（自测用）
```

## Golden case 定义

每个用例是 `dev/golden_cases/*.json`：

```json
{
  "id": "add_inventory",
  "prompt": "把 2L 牛奶加到冰箱，7 天后过期",
  "fixture": "empty",
  "assert": {
    "pantry.json": [
      {"path": "zones.cold.items", "contains": ["牛奶"]},
      {"path": "zones.cold.items", "count_equals": 1}
    ],
    "feedback.json": [
      {"path": "records", "record_exists": {"type": "ingredient-fact"}}
    ],
    "response.txt": [
      {"not_contains": ["鸡蛋"]}
    ]
  }
}
```

- `fixture`：`dev/fixtures/<name>/` 里的初始数据，被复制到临时 agent home 的 `pantry/data/`
- `assert` 目标文件：`*.json`（结构化断言）或 `response.txt`（agent 回复文本，manual 模式下手动放置）

### 断言谓词

结构化（`*.json`，作用于点号路径 `path`）：
- `contains` / `not_contains` — 数组内按 `name` 字段匹配
- `record_exists` — 数组内存在元素满足所有 `字段路径 == 值`
- `field_equals` — 路径解析值相等
- `count_gte` / `count_equals` — 数组长度

文本（`*.txt`）：`contains` / `not_contains` 子串检查。

## 原则

- 纯 Python 标准库，零依赖
- 断言只针对数据文件最终状态（objective ground truth），不评文案好坏
- executor 是薄接口：现在 manual，后续接 Hermes delegate / `claude -p` / `codex exec`
- 不进入 skill 分发

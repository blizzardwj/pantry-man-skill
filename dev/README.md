# dev/ — 开发期验证（dev-only，不进 skill 分发）

pantry-man-skill 的**开发期验证层**，与运行时脚本 `scripts/`（进分发）正交：

| 目录 | 用途 | 进分发 |
|------|------|--------|
| `dev/`（本目录） | 测 skill 本身对不对（回归） | 否 |
| `scripts/` | 帮 agent 运行时把操作做对（校验） | 是 |

## 内容

- `validate_static.py` — L1 静态校验（零 LLM，确定性），自动化 AGENTS.md 的 Verification Checklist
- `fixtures/` — 可复用的初始数据文件（空库存等，Phase 1 落地）
- `golden_cases/` — L2 行为黄金用例（Phase 1/2 落地）
- `run_golden.py` — L2 runner（Phase 1/2 落地）

## 用法

```bash
# 从仓库根目录（或任意目录）运行
python3 dev/validate_static.py
python3 dev/validate_static.py --data ~/.hermes/pantry/data/pantry.json   # 附加 schema 字段覆盖检查
```

## 原则

- 纯 Python 标准库，零依赖
- 只做确定性检查，不做需要 LLM 判断的事
- 不进入 skill 分发（安装 skill 不带走 dev/）

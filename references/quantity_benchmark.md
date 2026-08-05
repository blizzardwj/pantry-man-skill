# Quantity Benchmark（数量基准）

> Reference data for the 🛒 Shopping Plan **quantity check** step (see SKILL.md).
> All values are **general adult reference baselines** — informational, not medical advice.

## Adult Daily Reference Intake (Chinese Dietary Guidelines 2022)

| Category | Daily range | Notes |
|----------|-------------|-------|
| 蔬菜 vegetables | 300–500 g | Dark-colored greens ≈ half; cucumber & other cucurbits count as vegetables |
| 水果 fruit | 200–350 g | Juice does not replace fruit |
| 鱼/禽/肉 meat & fish | 120–200 g | Combined; includes eggs (1 egg ≈ 50 g); excludes soy products |
| 豆制品 soy | 25–35 g | As dried-soybean equivalent (北豆腐 ≈ 25% dry matter: 400 g tofu ≈ 100 g dry soy) |
| 谷类主食 staples | 200–300 g | Dry weight; rice / flour / oats / whole grains |
| 薯类 tubers | 50–100 g | Potato / sweet potato / yam; can replace part of staples |
| 蛋白质 protein | ≈ 1 g/kg body weight | 60 kg adult ≈ 60 g/day |
| 碳水化合物 carbs | 250–325 g | 2000 kcal × 50–65% |

## Segment Target Conversion

```
segment target range = daily range × segment days × household persons
```

- `segment days`: the current plan segment (default 3–4; check both gauges when ambiguous)
- `household persons`: `profile.json → household.persons` (default 1)

## Typical Piece Weights (convert 个/根 to grams)

| Item | Weight |
|------|--------|
| 桃子 / 苹果 peach, apple | ≈ 200 g/pc |
| 黄瓜 cucumber | ≈ 180 g/pc |
| 鸡蛋 egg | ≈ 50 g/pc |

## Category Assignment Rules

- 南瓜 / 冬瓜 / 胡萝卜 / 青椒 / 西兰花 / 菜心 / 生菜 / 秋葵 etc → **蔬菜**
- 黄瓜 → 蔬果两用; count as **蔬菜** when eaten as a cold dish (凉拌)
- 桃子 / 苹果 / 葡萄 etc → **水果**
- 土豆 / 红薯 / 山药 → **薯类** (root tubers count as non-refined carbs, may substitute staples)
- 鸡胸肉 / 鱼 / 虾 / 鸡蛋 → **鱼禽肉蛋**
- 豆腐 / 豆皮 / 豆浆 → **豆制品** (convert to dried-soybean equivalent)

## Check & Flag Rules

- Below range → ⚠️ note the shortfall
- Within [low, high] → ✅
- Above high, ≤ 1.5×high → ⚠️ suggest a converged quantity
- Above 1.5×high → ❌ suggest a converged quantity
- **Fresh items strict** (vegetables / fruit / fish): overage = spoilage risk, trim more aggressively
- **Shelf-stable staples lenient** (rice / dried goods / oils): overage is not waste, may keep
- **Soft flag only — never hard-block.** The user decides at the confirmation gate

> ⚠️ Reference baselines only, not medical advice. For chronic conditions, consult a doctor or registered dietitian.

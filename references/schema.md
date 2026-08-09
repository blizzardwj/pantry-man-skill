# Pantry Data Schema

Complete data structure definitions for pantry management.

## pantry.json

Food inventory organized by storage zone.

```json
{
  "meta": {
    "lastUpdated": "2026-04-01T17:45:00+08:00",
    "version": "1.0",
    "longCycleProbed": false
  },
  "zones": {
    "cold": {
      "name": "Refrigerator",
      "icon": "🧊",
      "items": []
    },
    "frozen": {
      "name": "Freezer",
      "icon": "❄️",
      "items": []
    },
    "ambient": {
      "name": "Ambient Storage",
      "icon": "📦",
      "items": []
    },
    "daily": {
      "name": "Daily Items",
      "icon": "🧴",
      "items": []
    }
  }
}
```

### Item Structure

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | string | Unique identifier | `item_a1b2c3` |
| `name` | string | Item name | `milk` |
| `quantity` | object | Amount with unit | `{"value": 1, "unit": "L"}` |
| `bought` | string | Purchase date | `2026-04-01` |
| `expires` | string | Expiry date | `2026-04-07` |
| `tags` | array | Categories for filtering | `["dairy", "breakfast"]` |
| `status` | string | fresh / expiring_soon / expired | `fresh` |

---

`meta.longCycleProbed` (boolean, optional): whether the one-time long-cycle staples probe (see SKILL.md Inventory Awareness) has been answered. Treat a missing value as `false` — existing data files remain valid.

## shopping.json

Shopping list organized by category.

```json
{
  "meta": {
    "lastUpdated": "2026-04-01T17:45:00+08:00"
  },
  "categories": {
    "food": {
      "name": "Food",
      "icon": "🥬",
      "items": []
    },
    "daily": {
      "name": "Daily Items",
      "icon": "🧴",
      "items": []
    }
  }
}
```

### Item Structure

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | string | Unique identifier | `shop_x9y8z7` |
| `name` | string | Item name | `tomato` |
| `quantity` | object | Amount with unit | `{"value": 3, "unit": "pcs"}` |
| `priority` | string | low / normal / high | `normal` |
| `added` | string | Date added to list | `2026-04-01` |
| `checked` | boolean | Marked as bought | `false` |
| `tags` | array | Categories for filtering | `["vegetable"]` |

---

## history/YYYY-MM.json

Purchase records organized by month.

```json
{
  "month": "2026-04",
  "records": [],
  "stats": {
    "totalSpent": 0.0,
    "recordCount": 0
  }
}
```

### Record Structure

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | string | Unique identifier | `rec_m5n6p7` |
| `date` | string | Purchase date | `2026-04-01` |
| `items` | array | List of purchased items | See below |
| `total` | number | Total amount spent | `27.0` |
| `store` | string | Store name (optional) | `Xiaoxiang` |
| `notes` | string | Additional notes (optional) | `weekend shopping` |

### Purchased Item Structure (within record.items)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `name` | string | Item name | `milk` |
| `quantity` | object | Amount with unit | `{"value": 1, "unit": "L"}` |
| `price` | number | Price of this item | `15.0` |

---

## profile.json

User dietary profile — drives weekly meal planning recommendations. **Optional file**: created by the agent during conversation (natural accumulation), not via a first-run questionnaire. The agent asks the user to confirm/correct it after the first weekly plan is generated.

```json
{
  "meta": {
    "lastUpdated": "2026-08-04T09:00:00+08:00"
  },
  "dietaryCulture": "chinese",
  "household": {
    "persons": 1
  },
  "health": {
    "familyHistory": ["diabetes", "heart-disease"],
    "conditions": [],
    "notes": "父辈有糖尿病和冠心病史，需控糖护心"
  },
  "preferences": {
    "avoid": ["refined-carbs", "unhealthy-fats"],
    "prefer": ["low-gi-carbs", "heart-healthy-fats", "high-protein"],
    "notes": "避免精制碳水，选择低升糖指数碳水"
  },
  "cookingStyle": ["steam", "boil", "cold-mix"],
  "shoppingRhythm": {
    "tripsPerWeek": 2,
    "daysPerTrip": "3-4"
  },
  "pairingTemplates": [
    {
      "id": "pt_x9y8z7",
      "meal": "breakfast",
      "pattern": "protein + root/tuber + 2-3 veg + fruit + homemade-yogurt",
      "source": "2026-08-05 早餐报告",
      "confirmed": true
    }
  ],
  "rules": [
    "生成采购计划前先确认人数"
  ],
  "confirmed": false
}
```

### Field Structure

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `meta.lastUpdated` | string | Last update datetime (ISO 8601 with tz) | `2026-08-04T09:00:00+08:00` |
| `dietaryCulture` | string | Diet culture keyword | `chinese` |
| `household.persons` | number | How many people the plan feeds (default 1) | `1` |
| `health.familyHistory` | array | Family genetic history keywords | `["diabetes", "heart-disease"]` |
| `health.conditions` | array | Known personal conditions | `[]` |
| `health.notes` | string | Free-text health notes (user language) | `父辈有糖尿病和冠心病史` |
| `preferences.avoid` | array | Foods to avoid (keywords) | `["refined-carbs", "unhealthy-fats"]` |
| `preferences.prefer` | array | Foods to prioritize | `["low-gi-carbs", "heart-healthy-fats"]` |
| `preferences.notes` | string | Free-text preference notes | `避免精制碳水` |
| `cookingStyle` | array | Preferred cooking methods | `["steam", "boil", "cold-mix"]` |
| `shoppingRhythm.tripsPerWeek` | number | Shopping trips per week | `2` |
| `shoppingRhythm.daysPerTrip` | string | Days covered per trip | `"3-4"` |
| `pairingTemplates` | array | Confirmed meal-structure templates (user-specific, from feedback; see SKILL.md Feedback section) | `[{"meal":"breakfast","pattern":"protein + root/tuber + 2-3 veg + fruit + yogurt"}]` |
| `rules` | array | User-level flow rules (confirmed, from feedback — never edits to SKILL.md) | `["生成采购计划前先确认人数"]` |
| `confirmed` | boolean | Whether user has confirmed the profile | `false` |

### Health & Preference Keywords (controlled vocabulary)

- **familyHistory / conditions**: `diabetes`, `heart-disease`, `hypertension`, `hyperlipidemia`, `liver-disease` (护肝), `none`
- **avoid**: `refined-carbs`, `unhealthy-fats` (saturated/trans), `high-sugar`, `alcohol`, `high-sodium`, `fried`
- **prefer**: `low-gi-carbs`, `heart-healthy-fats` (olive/fish/nuts), `high-protein`, `soluble-fiber` (水溶性膳食纤维: oats/seaweed/mushrooms/legumes), `low-fat`, `liver-friendly`
- **cookingStyle**: `cold-mix` (凉拌), `boil` (煮), `steam` (蒸), `griddle` (烙, 平底锅少油), `raw-when-possible` (能生吃不焯水), `blanch-over-steam` (能焯水不蒸), `minimal-cooking` (尽量缩短烹饪时间), `stir-fry` (炒), `roast`, `slow-cook`, `air-fry`

> ⚠️ Health-related recommendations are informational, not medical advice. The agent must include a disclaimer for users with chronic conditions (see SKILL.md Weekly Plan section).

---

## feedback.json

User feedback log — raw records of corrections, new facts, stock changes, and pairing/plan feedback (see SKILL.md Feedback section). Kept separate from profile.json: **profile holds the converged picture, feedback holds the raw log + landing trail**.

```json
{
  "meta": {
    "lastUpdated": "2026-08-05T13:30:00+08:00"
  },
  "records": []
}
```

### Record Structure

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | string | Unique identifier | `fb_x9y8z7` |
| `type` | string | `ingredient-fact` / `preference-correction` / `stock-change` / `pairing-feedback` | `stock-change` |
| `capturedAt` | string | Capture datetime (ISO 8601 with tz) | `2026-08-05T13:30:00+08:00` |
| `source` | string | User utterance summary | `苹果和黄瓜都已经吃完了` |
| `importance` | number | 1-5 (see anchors below) | `3` |
| `content` | string | Structured fact / correction | `黄瓜、苹果已耗尽` |
| `landing` | object | Where the feedback landed | See below |
| `status` | string | `active` / `decayed` / `evicted` | `active` |
| `mergedInto` | string | id of record this was merged into (optional) | `fb_a1b2c3` |

### landing Structure

| Field | Type | Description |
|-------|------|-------------|
| `target` | string | `pantry` / `shopping` / `profile` / `rule` (templates land on `profile` with detail noting `pairingTemplates`) |
| `applied` | boolean | Whether the data file was already updated |
| `detail` | string | What/where exactly |

### Type & Importance Anchors

| type | 判定要点 | 典型落点 |
|------|---------|---------|
| `ingredient-fact` | 新食材/新实体出现 | pantry |
| `preference-correction` | 推翻/修改既有画像或做法（含存储习惯）| profile / shopping |
| `stock-change` | 存量状态变化（吃完/耗竭/补货）| pantry / shopping |
| `pairing-feedback` | 对计划/搭配的满意度或改进建议 | rule / shopping |

importance 1-5: 5=画像/流程级（如"根茎类=非精制碳水"）；4=长期习惯（如"新鲜食材冷藏"）；3=状态事实（如"苹果吃完"）；2=一次性微调（如"鲈鱼→鲷鱼片"）；1=噪音/待观察（暂不沉淀）。

### Consolidation (four levers)

- **merge**: same entity across multiple records → entity data updated once, other records point to it via `mergedInto`
- **decay**: stock-change short-term facts → set `decayed` after refill/new purchase
- **eviction**: decayed records with no reference value → set `evicted` (log kept, never delete)
- **salience floor**: importance ≥ 4 records are never evicted by time alone

---

## Common Tags

### Food Categories
- `dairy` - Dairy products (milk, cheese, yogurt)
- `meat` - Meat (beef, pork, chicken)
- `seafood` - Fish and seafood
- `vegetable` - Vegetables
- `fruit` - Fruits
- `grain` - Grains, rice, pasta
- `condiment` - Sauces, spices, oil
- `snack` - Snacks
- `beverage` - Drinks
- `frozen` - Frozen foods

### Daily Items
- `cleaning` - Cleaning supplies
- `personal` - Personal care
- `kitchen` - Kitchen supplies
- `paper` - Paper products

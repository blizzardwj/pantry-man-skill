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
| `confirmed` | boolean | Whether user has confirmed the profile | `false` |

### Health & Preference Keywords (controlled vocabulary)

- **familyHistory / conditions**: `diabetes`, `heart-disease`, `hypertension`, `hyperlipidemia`, `liver-disease` (护肝), `none`
- **avoid**: `refined-carbs`, `unhealthy-fats` (saturated/trans), `high-sugar`, `alcohol`, `high-sodium`, `fried`
- **prefer**: `low-gi-carbs`, `heart-healthy-fats` (olive/fish/nuts), `high-protein`, `soluble-fiber` (水溶性膳食纤维: oats/seaweed/mushrooms/legumes), `low-fat`, `liver-friendly`
- **cookingStyle**: `cold-mix` (凉拌), `boil` (煮), `steam` (蒸), `griddle` (烙, 平底锅少油), `raw-when-possible` (能生吃不焯水), `blanch-over-steam` (能焯水不蒸), `minimal-cooking` (尽量缩短烹饪时间), `stir-fry` (炒), `roast`, `slow-cook`, `air-fry`

> ⚠️ Health-related recommendations are informational, not medical advice. The agent must include a disclaimer for users with chronic conditions (see SKILL.md Weekly Plan section).

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

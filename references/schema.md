# Pantry Data Schema

Data structure definitions for pantry management. All file paths below are relative to `[AGENT_HOME]/pantry/data/`.

## Shared item identity and unknown values

- `itemKey` is a stable food/product identity shared by pantry items, shopping items and purchased items. Reuse an existing key when identity is certain; otherwise assign a unique `food_…` (or `daily_…`) key. Names are display text; IDs identify individual entries.
- Do not merge merely similar foods or different forms (fresh milk vs milk powder, fresh vs dried mushrooms). Older entries without a key stay readable; attach a key only when identity is clear.
- `quantity` is `{ "value": 2, "unit": "pcs" }` when known and `null` when unknown. Unknown does not mean zero. In pantry.json, `value: 0` means the user reported eating it up (keep the unit if known, else `null`). Never infer a purchased amount from a planned one. Omit unknown dates, prices and totals; never invent them.

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
    "cold": { "name": "Refrigerator", "icon": "🧊", "items": [] },
    "frozen": { "name": "Freezer", "icon": "❄️", "items": [] },
    "ambient": { "name": "Ambient Storage", "icon": "📦", "items": [] },
    "daily": { "name": "Daily Items", "icon": "🧴", "items": [] }
  }
}
```

### Item Structure

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | string | Unique identifier | `item_a1b2c3` |
| `name` | string | Item name | `milk` |
| `itemKey` | string | Stable identity; required for new/updated entries | `food_milk` |
| `quantity` | object / null | Known amount, `value: 0` when eaten up, or `null` when unknown | `{"value": 1, "unit": "L"}` |
| `bought` | string | Purchase date (optional; omit if unknown or not a purchase) | `2026-04-01` |
| `expires` | string | Expiry date (optional). Passing it does not remove the item — see SKILL.md Inventory | `2026-04-07` |
| `tags` | array | Optional categories for filtering | `["dairy"]` |
| `status` | string | **Legacy — do not write.** Older files may contain fresh / expiring_soon / expired; ignore it. Expiry state is computed from `expires` | — |

`meta.longCycleProbed` (boolean, optional): whether the one-time staples question has been answered. Missing means `false`.

## shopping.json

Shopping list organized by category.

```json
{
  "meta": { "lastUpdated": "2026-04-01T17:45:00+08:00" },
  "categories": {
    "food": { "name": "Food", "icon": "🥬", "items": [] },
    "daily": { "name": "Daily Items", "icon": "🧴", "items": [] }
  }
}
```

### Item Structure

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | string | Unique identifier | `shop_x9y8z7` |
| `name` | string | Item name | `tomato` |
| `itemKey` | string | Stable identity shared with inventory | `food_tomato` |
| `quantity` | object / null | Requested amount; `null` when the user did not say | `{"value": 3, "unit": "pcs"}` |
| `priority` | string | Optional: low / normal / high | `normal` |
| `added` | string | Date added to list | `2026-04-01` |
| `checked` | boolean | The user reported buying it; does not assert the planned amount was bought | `false` |
| `tags` | array | Optional categories for filtering | `["vegetable"]` |

Older files may contain a `confirmation` object from a previous version; ignore it. Shopping-plan proposals now live only in the conversation until confirmed.

## history/YYYY-MM.json

Purchase records organized by month.

```json
{
  "month": "2026-04",
  "records": [],
  "stats": { "totalSpent": 0.0, "recordCount": 0 }
}
```

### Record Structure

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | string | Unique identifier | `rec_m5n6p7` |
| `date` | string | Purchase date | `2026-04-01` |
| `items` | array | Purchased items: `name`, `itemKey`, optional `quantity` (actual amount), optional `price` | `[{"name": "milk", "itemKey": "food_milk", "price": 15.0}]` |
| `total` | number | Total spent (optional; unknown is not zero) | `27.0` |
| `store` | string | Store name (optional) | `Xiaoxiang` |
| `notes` | string | Notes (optional) | `weekend shopping` |

On every write, `stats.recordCount` = number of records and `stats.totalSpent` = sum of known record totals.

## profile.json

Optional dietary profile, built gradually from what the user says.

```json
{
  "meta": { "lastUpdated": "2026-08-04T09:00:00+08:00" },
  "household": { "persons": 1 },
  "health": {
    "familyHistory": ["diabetes"],
    "conditions": [],
    "notes": "父辈有糖尿病史，需控糖"
  },
  "preferences": {
    "prefer": ["low-gi-carbs", "早餐: 洋葱、自制酸奶"],
    "avoid": ["refined-carbs"],
    "notes": ""
  },
  "cookingStyle": ["steam", "boil", "cold-mix"],
  "shoppingRhythm": { "tripsPerWeek": 2, "daysPerTrip": "3-4" },
  "exemplars": [
    {
      "id": "ex_a1b2c3",
      "name": "蒸鲷鱼山药",
      "ingredients": ["鲷鱼", "山药"],
      "method": "鲷鱼、山药同锅蒸，出锅撒少量欧芹海盐大蒜粉",
      "meal": "any"
    }
  ],
  "rules": ["生成采购计划前先确认人数"],
  "confirmed": false
}
```

| Field | Description |
|-------|-------------|
| `household.persons` | People the plan feeds (default 1) |
| `health.familyHistory` / `health.conditions` / `health.notes` | Health background, e.g. `diabetes`, `heart-disease`, `hypertension`, `hyperlipidemia`, `liver-disease` |
| `preferences.prefer` / `preferences.avoid` / `preferences.notes` | Short keywords or short phrases in the user's language, e.g. `low-gi-carbs`, `heart-healthy-fats`, `high-protein`, `soluble-fiber`, `refined-carbs`, `high-sodium`, `fried` |
| `cookingStyle` | Preferred methods, e.g. `cold-mix`, `boil`, `steam`, `griddle`, `raw-when-possible`, `stir-fry` |
| `shoppingRhythm.tripsPerWeek` / `shoppingRhythm.daysPerTrip` | Shopping rhythm (default 2 trips, 3–4 days each) |
| `exemplars` | Signature dishes the user confirmed: `id` (`ex_` prefix), `name`, `ingredients` (food names only), `method` (one sentence, fewest methods), `meal` (`breakfast` / `lunch` / `dinner` / `any`) |
| `rules` | The user's own workflow rules, followed in later plans |
| `confirmed` | Whether the user has confirmed the profile summary |

Older profiles may contain fields such as `dietaryCulture`, `pairingTemplates`, or exemplar `source` / `confirmed` / `addedAt` / `structure`. Keep them and read them as the user's stated preferences; new writes need not maintain them.

> ⚠️ Health-related recommendations are informational, not medical advice (see SKILL.md Ground Rules).

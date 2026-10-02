# Pantry Data Schema

Complete data structure definitions for pantry management. All file paths below are relative to `[AGENT_HOME]/pantry/data/`.

## Shared item identity and unknown values

- `itemKey` is a stable food/product identity shared by pantry items, shopping items, purchased items and food-specific feedback. Reuse an existing key when identity is certain; otherwise assign a unique `food_…` (or `daily_…`) key. Names are display text, IDs identify individual entries/batches. Reuse the key even after its pantry item was removed; search active feedback and shopping/history as needed.
- Do not merge merely similar foods or incompatible forms (fresh milk vs milk powder, fresh vs dried mushrooms). Confirmed aliases may share a key. Existing pantry/shopping/history entries without a key remain readable: attach a matching key only when identity is clear, otherwise leave the association unresolved. This does not migrate legacy feedback.
- Never infer purchase quantity from a proposed shopping quantity. Unknown inventory or directly requested shopping quantity is `null`; known quantity is `{ "value": 2, "unit": "pcs" }`. A generated shopping proposal still supplies an estimated quantity for confirmation. Unknown purchase date, expiry, price or total is omitted where marked optional. Unknown does not mean zero. Inventory updates use existing zones and storage habits; do not invent expiry or purchase dates.

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
| `itemKey` | string | Stable identity; required for new/updated entries | `food_milk` |
| `quantity` | object / null | Known amount with unit, or null when unknown | `{"value": 1, "unit": "L"}` |
| `bought` | string | Purchase date (optional; omit if unknown or not a purchase) | `2026-04-01` |
| `expires` | string | Expiry date (optional; omit if unknown) | `2026-04-07` |
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
| `itemKey` | string | Stable identity shared with inventory and feedback | `food_tomato` |
| `quantity` | object / null | Requested/proposed amount; null for an unspecified direct request | `{"value": 3, "unit": "pcs"}` |
| `priority` | string | low / normal / high | `normal` |
| `added` | string | Date added to list | `2026-04-01` |
| `checked` | boolean | Current shopping need marked as fulfilled by a reported purchase; does not assert that the planned quantity was bought | `false` |
| `tags` | array | Categories for filtering | `["vegetable"]` |

For a current report such as “买了苹果”, set a matching unchecked item to `checked=true` by default, even when the actual purchased amount is unknown. An explicit partial purchase or remaining need keeps it unchecked; change its requested quantity only when the remainder is known. A clearly historical purchase does not fulfill the current list by itself. See [purchase steps](feedback_flow.md#purchase-steps).

### confirmation (optional object)

Current or most recent shopping proposal context. Missing means no saved proposal. It is separate from `categories.*.items`: draft ingredients never enter the Daily Pairings pool. Retain it after confirmation for the current planning context; replace it for a genuinely new plan.

| Field | Type | Meaning |
|-------|------|---------|
| `id` | string | Unique proposal ID, e.g. `plan_a1b2c3`; reused across its adjustments |
| `status` | string | `open` / `confirmed` / `cancelled` |
| `proposedItems` | array | Not-yet-confirmed proposed items using the shopping item structure, with IDs assigned before writing; `checked=false` |
| `removedItemKeys` | array of strings | Distinct food keys removed from this proposal; excludes quantity changes and substitutions. Used to count deletions and prevent same-plan automatic re-addition; not a lasting preference |

Edits update the open proposal immediately. On partial confirmation, merge only approved items into `categories.food.items` and remove those from proposedItems; keep the rest open. On full confirmation, merge remaining approved items, empty proposedItems and set confirmed. An ordinary one-time list adjustment creates no feedback record. Ask the ≥3-deletion clarification at most once in the current confirmation conversation; a supplied reason is processed according to its actual content. Existing `clarificationAskedAt` values may remain in older files but are not required for new proposals. See [confirmation flow](feedback_flow.md#confirmation-flow).

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
| `total` | number | Total amount spent (optional; unknown is not zero) | `27.0` |
| `store` | string | Store name (optional) | `Xiaoxiang` |
| `notes` | string | Additional notes (optional) | `weekend shopping` |

### Purchased Item Structure (within record.items)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `name` | string | Item name | `milk` |
| `itemKey` | string | Stable identity shared with inventory and feedback | `food_milk` |
| `quantity` | object | Actual purchased amount (optional if unknown) | `{"value": 1, "unit": "L"}` |
| `price` | number | Price of this item (optional if unknown) | `15.0` |

For an ordinary current purchase with no other date supplied, use today's local date. An explicitly historical purchase uses its stated date; if that date is unknown, ask when a history entry is needed and never record it under today. Do not store date-less purchase facts as feedback. On every history write, recompute `stats.recordCount` as records.length and `stats.totalSpent` as the sum of known record totals. If any totals are missing, label the displayed sum as known spending, not complete monthly spending. A dated historical purchase alone does not establish today's inventory.

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
  "exemplars": [
    {
      "id": "ex_a1b2c3",
      "name": "蒸鲷鱼山药",
      "ingredients": ["鲷鱼", "山药"],
      "method": "鲷鱼、山药同锅蒸，出锅撒少量欧芹海盐大蒜粉",
      "meal": "any",
      "source": "2026-09-08 用户自创",
      "confirmed": true,
      "addedAt": "2026-09-08"
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
| `pairingTemplates` | array | Confirmed meal-structure templates (user-specific, from feedback; see [feedback_flow.md](feedback_flow.md)) | `[{"meal":"breakfast","pattern":"protein + root/tuber + 2-3 veg + fruit + yogurt"}]` |
| `exemplars` | array | User-verified concrete dishes — **instance-level** feedback (distinct from `pairingTemplates` structure). Consumed by Daily Pairings as in-context positive examples; multiple similar exemplars can later be promoted to a `pairingTemplates` entry (instance→structure). See [feedback_flow.md](feedback_flow.md) | `[{"name":"蒸鲷鱼山药","ingredients":["鲷鱼","山药"],"method":"同锅蒸…"}]` |
| `rules` | array | User-level flow rules (confirmed, from feedback — never edits to SKILL.md) | `["生成采购计划前先确认人数"]` |
| `confirmed` | boolean | Whether user has confirmed the profile | `false` |

### Exemplar Structure（实例级范例）

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | string | Unique identifier with the `ex_` prefix | `ex_a1b2c3` |
| `name` | string | Short name for retrieval and reference | `蒸鲷鱼山药` |
| `ingredients` | array | Main ingredients: food names only, without cooking verbs or dish names; seasonings belong in method | `["鲷鱼","山药"]` |
| `method` | string | One-sentence preparation using minimal grouped steps for the whole combination, including seasoning（组合级极简分组式）| `同锅蒸，出锅撒少量欧芹海盐大蒜粉` |
| `meal` | string | Applicable meal: `breakfast / lunch / dinner / any` | `any` |
| `source` | string | Source of the exemplar | `2026-09-08 用户自创` |
| `confirmed` | boolean | Whether confirmed; true when supplied by the user | `true` |
| `addedAt` | string | Date added | `2026-09-08` |
| `structure` | string | Optional tag grouping exemplars with the same structure; record only once the structure is established (RQ-6 promotion path, stage B) | `protein-fish + root-staple + steam` |

- **Reuse（消费方式）** (RQ-6; see [feedback_flow.md](feedback_flow.md)): when generating Daily Pairings, prioritize exemplars whose main ingredients are a subset of the current ingredient pool as in-context references (e.g., "照你上次的蒸鲷鱼山药做"). Multiple similar exemplars may be promoted to a `pairingTemplates` structure template (instance→structure).

### Health & Preference Keywords (controlled vocabulary)

- **familyHistory / conditions**: `diabetes`, `heart-disease`, `hypertension`, `hyperlipidemia`, `liver-disease` (护肝), `none`
- **avoid**: `refined-carbs`, `unhealthy-fats` (saturated/trans), `high-sugar`, `alcohol`, `high-sodium`, `fried`
- **prefer**: `low-gi-carbs`, `heart-healthy-fats` (olive/fish/nuts), `high-protein`, `soluble-fiber` (水溶性膳食纤维: oats/seaweed/mushrooms/legumes), `low-fat`, `liver-friendly`
- **cookingStyle**: `cold-mix` (凉拌), `boil` (煮), `steam` (蒸), `griddle` (烙, 平底锅少油), `raw-when-possible` (能生吃不焯水), `blanch-over-steam` (能焯水不蒸), `minimal-cooking` (尽量缩短烹饪时间), `stir-fry` (炒), `roast`, `slow-cook`, `air-fry`

> ⚠️ Health-related recommendations are informational, not medical advice. The agent must include a disclaimer for users with chronic conditions (see SKILL.md Weekly Plan section).

---

## feedback.json

Personalization signals, not a log of ordinary inventory, shopping, or purchase operations. Depletion after consumption can guide later replenishment; explicit preferences and evaluations guide future plans. Converged preferences live in `profile.json`. See the [Capture boundary](feedback_flow.md#capture-boundary) before writing a record.

```json
{
  "meta": {
    "version": "2.0",
    "lastUpdated": "2026-09-28T13:30:00+08:00"
  },
  "records": []
}
```

Keep existing v2 files and records. Older records may contain operational fields such as `landings[]` or `ingredient-fact` entries; preserve but do not execute the operational fields or add them to new records. Do not treat old `available` / `purchased` stock entries, simple `ingredient-fact` stock additions, or one-time list edits as preferences. For files older than v2, follow the [existing-data rule](feedback_flow.md#legacy-feedback). Normal log consolidation retains records.

### Record Structure

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | string | Unique signal ID | `fb_apple_empty` |
| `type` | string | New records: `stock-change` (consumption depletion only) / `preference-correction` / `pairing-feedback` | `stock-change` |
| `capturedAt` | string | Capture datetime (ISO 8601 with tz) | `2026-09-28T13:30:00+08:00` |
| `source` | string | Actual user utterance/summary; can be shared by atomic records | `苹果和黄瓜都吃完了` |
| `importance` | integer | 1–5; used only for feedback consolidation, never as a CRUD gate | `3` |
| `content` | string | This record's fact, scope and known details; preserve unresolved details here | `苹果已全部吃完` |
| `itemKey` | string | Required for a food-specific consumption signal; one food per record | `food_apple` |
| `stockEvent` | string | For new `stock-change` records, always `depleted`; omit for other types | `depleted` |
| `effectiveAt` | string / null | Required for depletion: current observation date/time with tz, or null when historical timing is unknown | `2026-09-28T13:30:00+08:00` |
| `status` | string | `active` (still useful) / `decayed` (superseded) / `evicted` (no longer used) | `active` |
| `mergedInto` | string | Optional duplicate fact's surviving record ID; same entity/event only, no cycles | `fb_existing` |

One new depletion record cannot contain both apples and cucumbers: split them and keep the same source. A later current restock ends only the affected food's older active depletion signal. Date-only precision or conflicting evidence may not establish ordering; do not decay a later depletion without evidence.

**Example — consumed apples available for selective replenishment:**

```json
{
  "id": "fb_apple_empty",
  "type": "stock-change",
  "capturedAt": "2026-09-28T13:30:00+08:00",
  "source": "苹果和黄瓜都吃完了",
  "importance": 3,
  "content": "苹果已全部吃完；黄瓜另记一条，可供以后选择性补购",
  "itemKey": "food_apple",
  "stockEvent": "depleted",
  "effectiveAt": "2026-09-28T13:30:00+08:00",
  "status": "active"
}
```

### Type & Importance Anchors

| Type | Classification criteria | Typical targets |
|------|---------|----------|
| `stock-change` | Explicitly consumed/depleted food; a selective replenishment signal, not an automatic lasting preference | later Shopping Plans |
| `preference-correction` | Explicit lasting food/cooking preference or correction to such a preference | profile.json and future plans |
| `pairing-feedback` | User evaluation of a pairing, plan or workflow; lasting rule only when stated or confirmed | current output and future plans |

Importance: 5 = confirmed profile/workflow rule; 4 = lasting preference; 3 = consumption signal or concrete evaluation; 2 = narrow feedback on one plan; 1 = tentative observation. Ordinary stock/clean-up operations get no score because they create no feedback record. Importance does not delay CRUD. Asking a question or receiving no answer is not user feedback.

### Consolidation

- **merge**: merge only duplicate records of the same signal; other records point to the retained record via mergedInto. Do not merge across foods or replenishment cycles.
- **decay**: explicit subsequent stock/replenishment facts mark only the superseded depletion records for the affected food as decayed. Buying apples affects only apples, not cucumbers. Confirming a shopping addition, skipping a purchase this time, deleting a list item or the passage of time does not trigger decay on its own.
- **eviction**: decayed records with no reference value may be marked evicted; retain the log rather than deleting it.
- **salience floor**: records with importance ≥4 must not be evicted solely because time has passed; explicit new facts may still supersede them.

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

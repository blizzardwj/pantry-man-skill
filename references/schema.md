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
| `checked` | boolean | Marked as bought | `false` |
| `tags` | array | Categories for filtering | `["vegetable"]` |

### confirmation (optional object)

Current or most recent shopping proposal context. Missing means no resumable proposal. It is separate from `categories.*.items`: draft ingredients never enter the Daily Pairings pool. Retain it after confirmation so resuming the same conversation does not reset the question flag; replace it only for a genuinely new plan.

| Field | Type | Meaning |
|-------|------|---------|
| `id` | string | Unique proposal ID, e.g. `plan_a1b2c3`; reused across its adjustments |
| `status` | string | `open` / `confirmed` / `cancelled` |
| `proposedItems` | array | Not-yet-confirmed proposed items using the shopping item structure, with IDs assigned before writing; `checked=false` |
| `removedItemKeys` | array of strings | Distinct food keys removed from this proposal; excludes quantity changes and substitutions. Used to count deletions and prevent same-plan automatic re-addition; not a lasting preference |
| `clarificationAskedAt` | string / null | ISO 8601 with tz, saved immediately before sending the one question; null means no question attempted. Not an answer or reason |

Edits update the open proposal immediately. On partial confirmation, merge only approved items into `categories.food.items` and remove those from proposedItems; keep the rest open. On full confirmation, merge remaining approved items, empty proposedItems and set confirmed. Record the authorized subset/IDs and confirmation update in feedback landings before changing files, so a retry never treats unconfirmed entries as approved. For the same confirmation.id, a non-null clarificationAskedAt must never be reset by an older snapshot or later edit; reconcile it before completing a pending confirmation update. A factual one-time list adjustment may be recorded as importance 2, with no invented preference. Deletion reasons already supplied are processed from the user's actual reply; there is no unanswered-question queue. See [confirmation flow](feedback_flow.md#confirmation-flow).

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

`date` must be the actual known purchase date; choose the month file from that date, not today's date. When the date is unknown, retain the known purchase facts in feedback.content and defer the history landing; do not block current stock updates. On every history write, recompute `stats.recordCount` as records.length and `stats.totalSpent` as the sum of known record totals. If any totals are missing, label the displayed sum as known spending, not complete monthly spending. Reuse a purchase record ID when completing missing details or retrying; a dated historical purchase alone does not establish today's inventory.

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
| `id` | string | Unique identifier（前缀 `ex_`）| `ex_a1b2c3` |
| `name` | string | 简短名，便于检索/引用 | `蒸鲷鱼山药` |
| `ingredients` | array | 主食材组合（只列食材名，不带做法动词/成菜名；调味料归 method）| `["鲷鱼","山药"]` |
| `method` | string | 做法一句话（组合级极简分组式，含调味）| `同锅蒸，出锅撒少量欧芹海盐大蒜粉` |
| `meal` | string | 适用餐次 `breakfast / lunch / dinner / any` | `any` |
| `source` | string | 来源 | `2026-09-08 用户自创` |
| `confirmed` | boolean | 是否确认（用户提供即 true）| `true` |
| `addedAt` | string | 添加日期 | `2026-09-08` |
| `structure` | string | （可选）同结构归组标签，固定下来时才记（RQ-6 上升路径阶段 B）| `protein-fish + root-staple + steam` |

- **消费方式**（RQ-6，见 [feedback_flow.md](feedback_flow.md)）：每日搭配生成时，凡范例的主食材 ⊆ 当前食材池 → 优先以 in-context 范例引用（"照你上次的蒸鲷鱼山药做"）；多道相似范例 → 可提升为 `pairingTemplates` 结构模板（instance→structure）。

### Health & Preference Keywords (controlled vocabulary)

- **familyHistory / conditions**: `diabetes`, `heart-disease`, `hypertension`, `hyperlipidemia`, `liver-disease` (护肝), `none`
- **avoid**: `refined-carbs`, `unhealthy-fats` (saturated/trans), `high-sugar`, `alcohol`, `high-sodium`, `fried`
- **prefer**: `low-gi-carbs`, `heart-healthy-fats` (olive/fish/nuts), `high-protein`, `soluble-fiber` (水溶性膳食纤维: oats/seaweed/mushrooms/legumes), `low-fat`, `liver-friendly`
- **cookingStyle**: `cold-mix` (凉拌), `boil` (煮), `steam` (蒸), `griddle` (烙, 平底锅少油), `raw-when-possible` (能生吃不焯水), `blanch-over-steam` (能焯水不蒸), `minimal-cooking` (尽量缩短烹饪时间), `stir-fry` (炒), `roast`, `slow-cook`, `air-fry`

> ⚠️ Health-related recommendations are informational, not medical advice. The agent must include a disclaimer for users with chronic conditions (see SKILL.md Weekly Plan section).

---

## feedback.json

Raw user facts and the trail of actual data updates; profile holds converged preferences. `status` concerns the fact, `landings[].applied` concerns one authorized update. No replenishment pending/dismissed state. See [feedback_flow.md](feedback_flow.md) for execution.

```json
{
  "meta": {
    "version": "2.0",
    "lastUpdated": "2026-09-28T13:30:00+08:00"
  },
  "records": []
}
```

Version 2 replaces the development-only singular `landing` format. Do not infer meaning from old applied values. Archive the old feedback file and initialize this seed per the [legacy-data rule](feedback_flow.md#legacy-feedback); no migration, no changes to other user data. Normal v2 log consolidation retains records.

### Record Structure

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | string | Unique event/fact ID; reused on retry | `fb_apple_empty` |
| `type` | string | `ingredient-fact` / `preference-correction` / `stock-change` / `pairing-feedback` | `stock-change` |
| `capturedAt` | string | Capture datetime (ISO 8601 with tz) | `2026-09-28T13:30:00+08:00` |
| `source` | string | Actual user utterance/summary; can be shared by atomic records | `苹果和黄瓜都吃完了` |
| `importance` | integer | 1–5; never an authorization flag | `3` |
| `content` | string | This record's fact, scope and known details; preserve unresolved details here | `苹果已全部吃完` |
| `itemKey` | string | Required for a food/product-specific fact; one key per stock record | `food_apple` |
| `stockEvent` | string | Required for stock-change: `depleted` / `available` / `purchased`; omit for other types | `depleted` |
| `effectiveAt` | string / null | Required for stock-change: known stock-fact date or ISO datetime with tz; null if historical timing unknown. Current-state assertion uses capture time; never a fabricated purchase date | `2026-09-28T13:30:00+08:00` |
| `landings` | array | Actual authorized updates, each independently applied; empty if none | See below |
| `status` | string | `active` (not superseded) / `decayed` (superseded fact) / `evicted` (no longer used); not purchase intent | `active` |
| `mergedInto` | string | Optional duplicate fact's surviving record ID; same entity/event only, no cycles | `fb_existing` |

One stock record cannot contain both apples and cucumbers as its actionable fact: split them and keep the same source. Multiple batches of one food may share itemKey; individual landings use itemId. Effective times with date-only precision or conflicting evidence may not establish ordering; do not overwrite current stock or decay a later depletion without sufficient evidence.

### landings[] Structure

Each element represents one actual write, not a candidate, question or request for permission.

| Field | Type | Description |
|-------|------|-------------|
| `target` | string | Exact data filename: `pantry.json`, `shopping.json`, `profile.json`, or `history/YYYY-MM.json` with the actual month; no arbitrary external path |
| `path` | string | Dot-separated object path to a scalar/object or an item array, e.g. `zones.cold.items`, `categories.food.items`, `preferences.avoid`, `confirmation`, `records` |
| `itemId` | string | Required when selecting an entry from an array of objects with IDs; e.g. item, shopping, purchase, exemplar/template ID. Never an array index. Omit when updating the field itself |
| `before` | JSON value | Value of the selected entry/field before this update; null means absent |
| `after` | JSON value | Complete final entry/field value; null means remove. Assigned ID must match itemId. Absolute final quantity, never a relative increment |
| `applied` | boolean | True only after verifying this update succeeded or target already equals after; false does not mean “recommend” or “unconfirmed” |
| `supersededBy` | string | Optional ID of a newer feedback fact that makes this update obsolete; excludes it from retry, does not falsify its historical applied value |

Compare only the selected entry/field, not a whole file. Preserve unrelated entries. For arrays of strings (e.g. preferences.avoid), before/after hold the field array; a concurrent mismatch must be reconciled, not overwritten. Metadata timestamps and derived history stats are updated along with the target file, outside these snapshots. Build any newly needed optional profile structure before selecting its field.

On recovery, first check newer facts. If current target equals after, mark applied; if it equals before and the operation still applies, write after; otherwise do not overwrite without resolving the conflict. Empty landings means no actual write was necessary or justified, not a pending shopping suggestion. An obsolete false landing retains false plus supersededBy; it must never delete replenished stock on retry.

**Example — inventory updated, depletion still available for selective reuse:**

```json
{
  "id": "fb_apple_empty",
  "type": "stock-change",
  "capturedAt": "2026-09-28T13:30:00+08:00",
  "source": "苹果和黄瓜都吃完了",
  "importance": 3,
  "content": "苹果已全部吃完；黄瓜另记一条",
  "itemKey": "food_apple",
  "stockEvent": "depleted",
  "effectiveAt": "2026-09-28T13:30:00+08:00",
  "landings": [
    {
      "target": "pantry.json",
      "path": "zones.cold.items",
      "itemId": "item_apple",
      "before": {"id": "item_apple", "itemKey": "food_apple", "name": "苹果", "quantity": {"value": 2, "unit": "pcs"}},
      "after": null,
      "applied": true
    }
  ],
  "status": "active"
}
```

### Type & Importance Anchors

| type | 判定要点 | 典型目标 |
|------|---------|----------|
| `ingredient-fact` | 新食材／新实体事实 | pantry.json |
| `preference-correction` | 更正偏好或本次操作；一次替换不是长期偏好 | profile.json / shopping.json |
| `stock-change` | 吃完、现有库存、购买；逐食材记录 | pantry.json / shopping.json / history |
| `pairing-feedback` | 用户对搭配、计划或流程的实际反馈 | profile.json / shopping.json |

importance：5=画像／流程级；4=长期习惯；3=状态事实；2=一次性微调；1=噪音／待观察（不沉淀）。明确操作不因低分延迟；提问本身和未回答均不是用户反馈，大量删除也不自动产生 imp 4。

### Consolidation

- **merge**：只归并同一事实／事件的重复记录，其他记录指向 mergedInto；不跨食材或补货周期，不重放实际数据更新。
- **decay**：明确的后续库存／补货事实只使被覆盖食材的旧耗尽记录 decayed。买回苹果只影响苹果，不影响黄瓜；确认加购、本次不买、删清单和时间流逝都不单独触发。
- **eviction**：无参考价值且没有尚需执行的落点的 decayed 记录可置 evicted；日志保留，不删除。
- **salience floor**：importance≥4 不仅因时间被淘汰；不妨碍被明确新事实取代。

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

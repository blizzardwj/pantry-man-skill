---
name: pantry-man
description: Manage home pantry inventory, shopping lists, and purchase history. Use when the user asks about (1) adding/viewing/searching inventory by zone (cold/frozen/ambient/daily), (2) managing shopping lists for food and daily items, (3) recording purchases and viewing purchase history, (4) checking expiry dates or items running low, (5) weekly meal planning — generating a weekly shopping plan and daily food pairings based on the user's dietary profile.
---

# Pantry Management

Manage home inventory, shopping lists, and purchase records.

## Data Location

All data files are under each agent's home directory at [AGENT_HOME]/pantry/data:

| File | Purpose |
|------|---------|
| `pantry.json` | Inventory (cold/frozen/ambient/daily zones) |
| `shopping.json` | Shopping list (food/daily categories) |
| `history/YYYY-MM.json` | Purchase records by month |

## First-Run Setup

Before executing ANY user request, check whether the pantry data directory exists. If it doesn't, initialize it silently — the user should never see a "file not found" error.

1. Check if `[AGENT_HOME]/pantry/data/` exists. If not, create the directory tree.
2. Check if `[AGENT_HOME]/pantry/data/pantry.json` exists. If not, create it with the empty seed structure from [schema.md](references/schema.md).
3. Check if `[AGENT_HOME]/pantry/data/shopping.json` exists. If not, create it with the empty seed structure.
4. Check if `[AGENT_HOME]/pantry/data/history/` exists. If not, create it.

After creating any missing files, confirm briefly to the user, e.g.:
"🧺 Your pantry is ready. Four zones set up (refrigerator, freezer, ambient, daily) — all empty for now. Try 'add milk to my fridge' to get started."

If all files already exist, skip silently — no need to announce.

## Core Operations

### Inventory

**View by zone:**
```
Read pantry.json → Format items from zones.cold/frozen/ambient/daily
```

**Add item:**
```
Read pantry.json → Append to zones.{zone}.items → Write back
```

**Remove item:**
```
Read pantry.json → Remove from zones.{zone}.items by id → Write back
```

**Check expiry:**
```
Read pantry.json → Filter items where expires date is within N days
```

### Shopping List

**View list:**
```
Read shopping.json → Format items from categories.food/daily
```

**Add item:**
```
Read shopping.json → Append to categories.{category}.items → Write back
```

**Mark as bought:**
```
Read shopping.json → Set item.checked = true OR remove item → Write back
```

### Purchase History

**Record a purchase:**
```
1. Determine current month file (YYYY-MM.json), create if not exists
2. Read the file → Append record to records array → Update stats → Write back
3. Verify JSON is valid before save (e.g., no missing commas)
```

**View history:**
```
Read history/YYYY-MM.json → Format records
```

**Monthly stats:**
```
Read history/YYYY-MM.json → Return stats.totalSpent and stats.recordCount
```

## Weekly Plan (Weekly Meal Planning)

Generates a weekly shopping plan and daily food pairings based on the user's dietary profile. This is the skill's value-generating feature: the plan fills the shopping list, so the user confirms and adjusts instead of entering data item by item.

### User Profile (profile.json)

Stored at `[AGENT_HOME]/pantry/data/profile.json` (see [schema.md](references/schema.md) for structure). **Optional and lightweight — never conduct a first-run questionnaire.**

- Build the profile **gradually from conversation**: when the user mentions dietary preferences, health history, or cooking style, record it (e.g., user says "我不吃精制碳水" → `preferences.avoid += "refined-carbs"`).
- If `profile.json` does not exist and the user asks for a weekly plan, create it with only what you already know (can be nearly empty) and **generate the plan anyway** — do not block on missing profile fields.
- After the **first** generated plan, briefly show the profile summary and ask the user to confirm or correct it (one confirmation beats a questionnaire). Set `confirmed: true` after confirmation.
- If `confirmed` is false, the plan is a proposal — invite corrections.

### Generating a Weekly Plan

Trigger: user asks for a weekly shopping plan / "这周买什么" / "本周吃什么".

**Step 1 — Load context:**
```
1. Read profile.json (create if missing, see above)
2. Read shopping.json → note unchecked items (already needed — avoid duplicates)
3. Phase 2 (when implemented): read pantry.json → note remaining stock to avoid re-buying
```

**Step 2 — Shopping rhythm:**
```
Use profile.shoppingRhythm (default: 2 trips/week, 3-4 days per trip, e.g. Sunday + Wednesday)
→ Split the week into segments (e.g., Sun-Wed, Wed-Sat)
```

**Step 3 — Recommend items by category** (each with **variety AND approximate quantity**):

| Category | Chinese examples | Notes |
|----------|-----------------|-------|
| 蔬菜 vegetables | 南瓜、冬瓜、香菇、海带、菜心、生菜 | Prioritize per profile.prefer / avoid |
| 水果 fruit | 桃子、黄瓜（果蔬）、青椒 | Seasonal when applicable |
| 蛋白质 protein | 鸡蛋、鸡胸肉、虾皮、鱼、豆制品 | High-quality, low-saturated-fat sources |
| 油脂 oils/fats | 橄榄油、坚果（南瓜子等）、鱼油类食材 | Heart-healthy unsaturated fats |
| 主食 staples | 糙米、燕麦、全麦、薯类 | Low-GI per profile (avoid refined carbs) |

Apply the profile: avoid `refined-carbs`/`unhealthy-fats` → choose `low-gi-carbs`/`heart-healthy-fats`/`high-protein`/`high-fiber`. For each item, give a **rough quantity** (e.g., 南瓜 500g, 鸡蛋 10枚, 鸡胸肉 500g) — enough for the segment's meals.

**Step 4 — Daily pairings:**
```
For each day, propose 2-3 dishes/meals as a combo with a short rationale
(e.g., Monday: 蒸碗菜（南瓜+冬瓜+香菇+海带+虾皮+水煮蛋+鸡胸肉）+ 水果沙拉碗（桃子+黄瓜+青椒+生菜）+ 水煮菜+坚果碗（菜心+南瓜子）
Rationale: 利尿、膳食纤维、高吸收率蛋白质、低热量)
```

**Step 5 — Write to shopping list:**
```
Append recommended items (with quantities) to shopping.json categories.food.items
→ Tell the user: "已加入购物清单，可修改数量或删除"
```

**Step 6 — Confirm profile (first plan only):**
```
Show profile summary → ask user to confirm/correct → update profile.json → set confirmed: true
```

### ⚠️ Health Disclaimer

Health-related recommendations (diabetes, heart disease, liver conditions, etc.) are **informational, not medical advice**. Always include with any plan for users with chronic conditions:

> "以上为一般性饮食建议，不构成医疗建议。如有重大健康问题，请咨询医生或注册营养师。"

## Item ID Generation

Use format: `{type}_{random_6_chars}` (e.g., `item_a1b2c3`, `shop_x9y8z7`, `rec_m5n6p7`)

## Timestamp Format

- Dates: `YYYY-MM-DD` (e.g., `2026-04-01`)
- Datetimes: ISO 8601 with timezone (e.g., `2026-04-01T17:45:00+08:00`)

## References

- See [schema.md](references/schema.md) for complete data structure definitions.

## Scheduled Reminders (Recommended)

Use cron jobs for time-specific reminders. These align with user's daily routine.

### Shopping List Reminder

Remind user to check shopping list during lunch break and after work:

```bash
# Add cron jobs (Asia/Shanghai timezone)
cron add "0 12 * * *" "Check pantry/data/shopping.json for unchecked items. If count > 0, remind: 🛒 Shopping List Reminder: You have {count} items to purchase"
cron add "30 17 * * *" "Check pantry/data/shopping.json for unchecked items. If count > 0, remind: 🛒 Shopping List Reminder: You have {count} items to purchase"
```

### Expiry Alert

Remind user in the morning about items expiring soon:

```bash
cron add "0 8 * * *" "Check pantry/data/pantry.json for items expiring within 3 days. If found, alert: ⚠️ {count} item(s) expiring soon: {item names}"
```

### Low Stock Alert (Optional)

Check if essential items are running low:

```bash
cron add "0 9 * * 1" "Check pantry/data/pantry.json for low stock items. Suggest adding to shopping list if needed."
```

## Heartbeat Tasks (Alternative)

For periodic checks without specific time requirements, use `HEARTBEAT.md`:

### Inventory Cleanup

Periodically clean up expired items:

```
1. Read pantry/data/pantry.json
2. Remove items where expires date has passed
3. Update the file
```

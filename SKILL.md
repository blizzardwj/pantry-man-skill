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

**Cold-start probe on view (see Inventory Awareness below):**
If the inventory has NO long-cycle items recorded (empty, or only short-cycle fresh items) and `meta.longCycleProbed` is not `true` → fire the one-time friendly probe along with the (empty) inventory, then show the view. Never block the view on the probe.

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

### Inventory Awareness (stock-aware planning)

Long-cycle staples (dry goods, oils, nuts, grains) are stocked for weeks, not days — recommending them every week causes duplicate purchases. Short-cycle fresh items (vegetables, fruit, fish, tofu) are bought weekly anyway, so stock awareness matters little for them.

**Stock-aware rule:**
```
Read pantry.json → for each long-cycle category (oils/fats, nuts, staples,
dry goods), if the item already exists in ambient/daily zones → SKIP it in
the plan (or suggest a refill only if quantity is nearly depleted).
Fresh items are always recommended per the weekly rhythm.
```

**Cold-start probe (general rule — fires on ANY inventory read, not just planning):**
When pantry.json has no long-cycle items recorded (empty, or only short-cycle fresh items) and `meta.longCycleProbed` is not `true`, probe with ONE friendly opening — then proceed with whatever the user asked for. Never audit the whole pantry, never block the request.

- **Trigger points:** Viewing inventory (primary), and Weekly Plan Step 1 (below). Both share the same flag — whichever comes first fires the probe once.
- **Flag semantics:** set `meta.longCycleProbed: true` in pantry.json once the user RESPONDS — whether they confirm items or say there are none. If the user doesn't answer, leave it unset; the next natural touchpoint may try the opening once more.
- **Outcome:** confirmed items are recorded into the ambient zone (no expiry needed for staples) → future plans skip them; "none" → plans recommend staples normally (nothing in stock to skip).

**UX copy pattern (de-AI-fied, 4 turns):**
1. Acknowledge the user's identity first — never open with a data request
2. Use empathetic inference instead of a direct question (lowers answer pressure; user only confirms)
3. Frame the request as a service — value belongs to the user ("我来帮你记住")
4. State the user benefit, not the agent's logic (never say "规划时我会避开")
   - 示例开场 (long-cycle cold-start):
     "初次接触，像你这样注重健康饮食的人，我觉得应该有干货和食用油囤货。我来帮你记住这些，更好地为您提供食材搭配。"
   - Record what the user confirms into pantry.json (ambient zone, no expiry needed for staples) and set `meta.longCycleProbed: true` → future plans skip them (or recommend them if the user said none).

**Stock grows through daily behaviors, not audits:**
- Purchase → also append to pantry.json (buy = restock)
- Expiry alert → ask "吃完了吗？" → remove from inventory (consume = deplete)
- Never require a one-time full inventory audit.

### Generating a Weekly Plan

Trigger: user asks for a weekly shopping plan / "这周买什么" / "本周吃什么".

**Step 1 — Load context:**
```
1. Read profile.json (create if missing, see above)
2. Read shopping.json → note unchecked items (already needed — avoid duplicates)
3. Read pantry.json → note existing long-cycle stock (ambient/daily zones)
   → Apply the stock-aware rule above: skip items already in stock
   → If pantry has no long-cycle items recorded and meta.longCycleProbed
     is not true → use the cold-start UX opening (see Inventory
     Awareness; it may already have fired on an earlier inventory view)
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

Apply the profile: avoid `refined-carbs`/`unhealthy-fats` → choose `low-gi-carbs`/`heart-healthy-fats`/`high-protein`/`soluble-fiber` (适量水溶性膳食纤维). For each item, give a **rough quantity** (e.g., 南瓜 500g, 鸡蛋 10枚, 鸡胸肉 500g) — enough for the segment's meals. **Skip long-cycle items already in stock** (per the stock-aware rule above); when a staple (oils/nuts/grains) is skipped, mention it briefly (e.g., "橄榄油已有库存，未列入") so the user sees the plan is stock-aware.

**Step 4 — Daily pairings (food combos, not recipes):**
```
For each day, propose ingredient COMBOS (not dish names) with a short
rationale, then the SIMPLEST healthy preparation in 1-2 short phrases.

FIXED 3-PART PATTERN — every pairing MUST include all three:
  ① 食材组合 ingredients  ② 价值 value/why  ③ 做法 simplest preparation

Format per day:
[早/午/晚] 食材1 + 食材2 + 食材3（价值：为什么这样搭）→ 做法：一句话
(e.g., 午餐: 鸡胸肉 + 香菇 + 西兰花（价值：高蛋白+水溶性纤维+护肝）→ 做法：鸡胸肉平底锅少油烙片，香菇西兰花焯水2分钟拌橄榄油
       晚餐: 魔芋丝 + 黄瓜 + 虾皮（价值：低GI饱腹+清爽+补钙）→ 做法：魔芋焯水30秒，黄瓜生切，虾皮拌入)

Rules:
- Combos honor profile.prefer/avoid and cookingStyle (e.g., 凉拌/煮/蒸/烙, 能生吃不焯水)
- 价值 = the nutritional/health reason for THIS combo, 1 short phrase
- 做法 = the simplest healthy method, 1-2 short phrases, not a recipe
- Prefer raw over blanched, blanch over steamed/boiled, per profile (short cooking time)
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

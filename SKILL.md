---
name: pantry-man
description: Manage home pantry inventory, shopping lists, and purchase history. Use when the user asks about (1) adding/viewing/searching inventory by zone (cold/frozen/ambient/daily), (2) managing shopping lists for food and daily items, (3) recording purchases and viewing purchase history, (4) checking expiry dates or items running low, (5) meal planning — shopping plans (采购计划) and daily food pairings (每日搭配) as independent features, plus the weekly plan (周计划) orchestrator that chains them per the user's shopping rhythm, all based on the user's dietary profile and current stock.
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
| `feedback.json` | User feedback log (corrections, new facts, stock changes, pairing feedback — see [feedback_flow.md](references/feedback_flow.md)) |

## First-Run Setup

Before executing ANY user request, check whether the pantry data directory exists. If it doesn't, initialize it silently — the user should never see a "file not found" error.

1. Check if `[AGENT_HOME]/pantry/data/` exists. If not, create the directory tree.
2. Check if `[AGENT_HOME]/pantry/data/pantry.json` exists. If not, create it with the empty seed structure from [schema.md](references/schema.md).
3. Check if `[AGENT_HOME]/pantry/data/shopping.json` exists. If not, create it with the empty seed structure.
4. Check if `[AGENT_HOME]/pantry/data/history/` exists. If not, create it.
5. Check if `[AGENT_HOME]/pantry/data/feedback.json` exists. If not, create it with the empty seed structure (`{"meta": {"lastUpdated": "<now>"}, "records": []}`).

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

## Feedback Capture & Reuse（反馈沉淀与复用）

User corrections, new facts, and preferences are the highest-value signal for profile convergence — capture them when they happen, so plans improve without the user re-entering data. **Raw log**: `feedback.json`.

**反馈处理是本 skill 的运行重点——完整状态机独立维护在 [feedback_flow.md](references/feedback_flow.md)，涉及反馈捕获、落点、整理、消费时必读。** 核心结构摘要：

- **三层 hooks（术语）**：agent 无常驻进程，反馈处理挂在宿主流程的自然执行点上——`capture hook`（对话中即时捕获）→ `threshold hook`（同日阈值静默整理）→ `review hook`（生成计划/搭配前兜底消费）。写侧（capture/threshold）与读侧（review）双向触发，同一状态机首尾相接。
- **落点**：个性化输出（偏好/模板/用户级流程规则）始终沉淀到用户数据（`profile.json` / `pantry.json` / `shopping.json`）——**never edit SKILL.md for a user's rules**；SKILL.md 保持跨用户通用框架。
- 📖 **完整流程（信号表 / 冲突避免 / 落点判定 / 三层 hooks / 支持规则 / 闭环图）见 [feedback_flow.md](references/feedback_flow.md)——生成搭配与采购计划前、捕获反馈落点时必读。**

SKILL.md 只承载通用框架——任何用户的个性化规则、模板、偏好都沉淀在用户数据中。

## Meal Planning

Two independent features — 🛒 采购计划 Shopping Plan and 🍽 每日搭配 Daily Pairings — plus 📆 周计划 Weekly Plan, an orchestrator that chains them per the user's shopping rhythm. **Order is fixed: shopping list first, pairings second.** Pairings are derived from the confirmed list (素材→组合 dependency) — never the other way around. Each feature has its own trigger, confirmation gate, and adjustment path, so the user can run any of them standalone (e.g., "今晚吃什么" only needs Daily Pairings).

This is the skill's value-generating feature: planning fills the shopping list, so the user confirms and adjusts instead of entering data item by item.

### User Profile (profile.json)

Stored at `[AGENT_HOME]/pantry/data/profile.json` (see [schema.md](references/schema.md) for structure). **Optional and lightweight — never conduct a first-run questionnaire.**

- Build the profile **gradually from conversation**: when the user mentions dietary preferences, health history, or cooking style, record it (e.g., user says "我不吃精制碳水" → `preferences.avoid += "refined-carbs"`).
- `household.persons` (default 1): how many people the plan feeds — required by
  the Shopping Plan quantity check. Infer from conversation (e.g., "一个人吃")
  or default to 1.
- If `profile.json` does not exist and the user asks for any meal planning feature (采购计划/每日搭配/周计划), create it with only what you already know (can be nearly empty) and **generate the plan anyway** — do not block on missing profile fields.
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

- **Trigger points:** Viewing inventory (primary), and 采购计划 Shopping Plan step 3 (below). Both share the same flag — whichever comes first fires the probe once.
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

### 🛒 采购计划 Shopping Plan (independent feature)

Trigger: user wants to buy ingredients / "列个采购清单" / "帮我看看这周买什么" — standalone, or called by the Weekly Plan orchestrator.

Flow:
```
1. Read profile.json (create if missing, see User Profile above) → note prefer/avoid
   rules and `rules` (user-level flow rules — follow them; never SKILL.md edits)
2. Read shopping.json → note unchecked items (already needed — avoid duplicates)
3. Read pantry.json → apply the stock-aware rule: skip long-cycle items already
   in stock (ambient/daily zones); briefly mention skipped staples (e.g.,
   "橄榄油已有库存，未列入") so the user sees the plan is stock-aware
   → If pantry has no long-cycle items recorded and meta.longCycleProbed is
     not true → fire the cold-start probe (see Inventory Awareness; it may
     already have fired on an earlier inventory view)
4. Determine the segment length (default 3-4 days; Weekly Plan passes its segment)
5. Recommend items by category, each with **variety AND approximate quantity**:
```

| Category | Chinese examples | Notes |
|----------|-----------------|-------|
| 蔬菜 vegetables | 南瓜、冬瓜、香菇、海带、菜心、生菜 | Prioritize per profile.prefer / avoid |
| 水果 fruit | 桃子、黄瓜（果蔬）、青椒 | Seasonal when applicable |
| 蛋白质 protein | 鸡蛋、鸡胸肉、虾皮、鱼、豆制品 | High-quality, low-saturated-fat sources |
| 油脂 oils/fats | 橄榄油、坚果（南瓜子等）、鱼油类食材 | Heart-healthy unsaturated fats |
| 主食 staples | 糙米、燕麦、全麦、薯类 | Low-GI per profile (avoid refined carbs) |

Apply the profile: avoid `refined-carbs`/`unhealthy-fats` → choose `low-gi-carbs`/`heart-healthy-fats`/`high-protein`/`soluble-fiber` (适量水溶性膳食纤维). For each item, give a **rough quantity** (e.g., 南瓜 500g, 鸡蛋 10枚, 鸡胸肉 500g) — enough for the segment's meals.

```
6. **PLAN-TIME REVIEW — feedback backfill (only when today has feedback):**
   Run the Review hook per [feedback_flow.md](references/feedback_flow.md):
   a. Retrieve active feedback with imp ≥ 3 → backfill any missed landing
   b. Depleted candidates: stock-change "吃完" records (`applied: false`) → list
      them in their category with note "上次已吃完，可补" (user decides at the gate)
   c. Clarification: if the last confirmation gate had ≥ 3 deletions → ask ONE
      high-value question before generating (largest-impact dimension only)
7. **QUANTITY CHECK — benchmark before the gate:**
   Read [quantity_benchmark.md](references/quantity_benchmark.md) (adult daily
   reference ranges, typical piece weights, category assignment). For each
   category, compute the segment target range = daily range × segment days ×
   `household.persons` (default 1), compare with the proposed total, and show
   a compact check report: ✅ within range / ⚠️ slightly over or under / ❌ way
   off — each with a suggested converged quantity.
   - Fresh items (vegetables, fruit, fish) — strict: overage means spoilage
   - Shelf-stable staples (rice, dried goods, oils) — lenient: extra stock is fine
   - Soft flag only, never hard-block — the user decides at the confirmation gate
   Example: "蔬菜 914g/天 vs 300–500 ❌ → 建议 ~1600g（绿叶菜减半）"
8. **CONFIRMATION GATE — do NOT write to shopping.json yet:**
   Show the proposed list (category + item + quantity, with the check report
   from step 7) and ask the user to confirm or adjust (quantities, items,
   budget). Only after the user confirms, append the (adjusted) items to
   shopping.json categories.food.items, then tell the user: "已加入购物清单，
   可继续修改数量或删除"
```

### 🍽 每日搭配 Daily Pairings (independent feature)

Trigger: "今晚吃什么" / "明天怎么搭" / meals for this segment — standalone, or called by the Weekly Plan orchestrator after its shopping plan is confirmed.

**Ingredient pool (hard constraint):** pairings draw ONLY from
- the current segment's confirmed shopping items (shopping.json categories.food.items — the unchecked items), plus
- pantry stock (esp. long-cycle staples: dried goods, oils, nuts).

If the shopping list has no items for the current segment, tell the user to generate/confirm a 采购计划 first — never propose ingredients that are neither bought nor stocked (素材→组合 dependency).

Flow:
```
1. Read shopping.json (current segment items) + pantry.json (stock) → build the ingredient pool
   → Also read profile.json: `pairingTemplates`, prefer/avoid/cookingStyle
   → If today has feedback, run the Review hook first (see [feedback_flow.md](references/feedback_flow.md))
2. For each day in the segment, propose 3 meals (早/午/晚) with THREE-LEVEL
   REFERENCE (template > profile > generic — see [feedback_flow.md](references/feedback_flow.md)):
     ① 模板层 template: confirmed `pairingTemplates` for that meal define the
        structure (e.g. breakfast = protein + root/tuber + 2-3 veg + fruit +
        yogurt); multiple templates for one meal → rotate to avoid repetition
     ② 画像层 profile: prefer/avoid/cookingStyle govern ingredient choice & method
     ③ 通用准则层 generic: FIXED 3-PART PATTERN — every pairing MUST include:
        ① 食材组合 ingredients  ② 价值 value/why  ③ 做法 simplest preparation
   Conflict: templates are structure, never break health constraints —
   profile/health rules win, template downgraded to reference.
3. Display as per-day blocks with meals as LIST items — the format example
   below shows SHAPE ONLY: ingredients are category placeholders, generate
   your own combos, values, and cooking wording from stock + profile
   (never reuse this example's items or phrasing):
   📅 周三（8/5）
   - 早餐：主食类 + 蛋白类 + 蔬果类（价值：为什么这样搭）→ 做法：一句话
   - 午餐：蛋白类 + 绿叶菜类 + 根茎类主食（价值：营养理由一句话）→ 做法：蛋白蒸或烙，绿叶菜焯水拌油
   - 晚餐：低GI主食类 + 清爽蔬菜类 + 干鲜类（价值：营养理由一句话）→ 做法：主食焯水，蔬菜生切，干鲜拌入
4. Confirmation & adjustment:
   - Invite the user to adjust any specific meal (e.g., "周四晚餐换个素的")
     → regenerate ONLY that meal, keep the rest unchanged
   - If the user later changes the shopping list (adds/removes items), regenerate
     the affected meals — pairings must stay consistent with the confirmed list
```

Rules:
- Combos honor profile.prefer/avoid and cookingStyle (e.g., 凉拌/煮/蒸/烙, 能生吃不焯水)
- 价值 = the nutritional/health reason for THIS combo, 1 short phrase
- 做法 = the simplest healthy method, 1-2 short phrases, not a recipe
- Prefer raw over blanched, blanch over steamed/boiled, per profile (short cooking time)

### 📆 周计划 Weekly Plan (orchestrator)

Trigger: "这周买什么" / "本周怎么安排" / weekly planning. This feature chains the two independent features above — it does NOT duplicate their logic.

Flow:
```
1. Load context:
   - Read profile.json (create if missing, see User Profile)
   - Read shopping.json → note unchecked items (avoid duplicates)
   - Read pantry.json → apply the stock-aware rule; fire the cold-start probe
     if needed (see Inventory Awareness; may already have fired)
2. Split the week by profile.shoppingRhythm (default: 2 trips/week, 3-4 days per
   trip, e.g. Sunday + Wednesday) → segments (e.g., Sun-Wed, Wed-Sat)
3. Plan ONE segment per invocation (the next upcoming trip), segment by segment:
   a. Call 🛒 采购计划 Shopping Plan for this segment
      → present list → user confirms/adjusts → write to shopping.json
   b. Call 🍽 每日搭配 Daily Pairings for this segment
      → present per-day meal lists → user confirms/adjusts
4. Do NOT dump the whole week at once — the second segment is planned when the
   user is ready ("继续下一段"), so its list and pairings can reflect what was
   actually bought and consumed in the first segment. If the user explicitly
   asks to see the whole week up front, draft all segments but still confirm
   each segment's list before writing.
5. First plan only: show profile summary → ask user to confirm/correct →
   update profile.json → set confirmed: true (see User Profile)
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
- See [quantity_benchmark.md](references/quantity_benchmark.md) for the adult
  daily intake baselines used by the Shopping Plan quantity check.

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

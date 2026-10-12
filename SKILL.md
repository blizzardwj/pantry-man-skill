---
name: pantry-man
description: Track the user's own household food stock, shopping list and purchases, and plan what to buy and eat from them. Use when the user (1) adds, removes, views or searches items at home by zone (cold/frozen/ambient/daily), or asks what is expiring or running low; (2) edits the shopping list, reports buying something (including by sending a receipt photo), or views purchase history; (3) reports eating something up, sends a photo of groceries or the fridge, or states food preferences for future plans; (4) asks for a shopping plan (采购计划), what to eat from what they have (每日搭配, e.g. 今晚吃什么), or a weekly plan (周计划); (5) asks how to eat or pair a food in light of their own stock or dietary profile (食材咨询). Not for general recipe or cooking questions unrelated to the user's own stock or profile.
---

# Pantry Management

Track what the user has at home, what they need to buy and what they bought, and plan purchases and meals from that.

## Data

All files live in `[AGENT_HOME]/pantry/data/`. Field definitions: [schema.md](references/schema.md).

| File | Holds |
|------|-------|
| `pantry.json` | What is at home, by zone (cold / frozen / ambient / daily). Eaten-up foods stay with quantity 0 |
| `shopping.json` | What to buy (food / daily) |
| `history/YYYY-MM.json` | Purchase records by month |
| `profile.json` | Optional: household size, health, preferences, cooking style, shopping rhythm, signature dishes, the user's own rules |

A `feedback.json` left by older versions is no longer used; leave it untouched.

**Creating data:** read-only requests never create files — a missing file reads as its empty seed from schema.md. Before the first write, create the directory, `history/`, and any missing `pantry.json` / `shopping.json` seed, then mention it briefly with the result ("🧺 Your pantry is set up. Milk is now in the fridge.").

## Ground Rules

These override habit; each exists because the obvious behavior is wrong here.

1. **Change data only from what the user said.** A receipt photo counts as saying it; other photos do not (see Photos). Keep item names in the user's own words — never translate them ("牛奶" stays 牛奶; "milk" stays milk). Never invent quantities, dates, prices or totals. Unknown is `null` or omitted — never 0.
2. **Keep facts apart.** "家里有" is not a purchase; "买了" is not a preference; adding to the list is not buying; removing something once is not a dislike.
3. **Expired is not gone; thrown away is not eaten.**
4. **Eaten up → quantity 0, not deleted.** It is a hint for later shopping plans; a restock replaces it.
5. **Not bought means not at home.** A meal for today uses stock only.
6. **Your suggestions need confirmation; the user's edits do not.** Write a generated shopping plan only after the user confirms it; apply explicit edits directly.
7. **One food, one `itemKey`**, reused across pantry, list and history. Keep different forms apart (fresh vs dried mushrooms).
8. **The user's rules go to profile.json**, never into this skill.
9. **Health disclaimer:** when advice involves a chronic condition in the profile, add (in the user's language) "以上为一般性饮食建议，不构成医疗建议。如有重大健康问题，请咨询医生或注册营养师。"
10. **Reply in the user's language.** The Chinese phrases in this skill and its references — questions, labels such as 已吃完, 待买, 上次吃完，可补, 早／午／晚 — show the meaning, not fixed wording; say them in the user's language.

## Operations

### Inventory — pantry.json

- **Add / update:** match by `itemKey` and update the existing entry instead of duplicating it. Restocking an eaten-up item sets the new quantity (`null` if unknown).
- **Eaten up** ("苹果吃完了"): set that food's quantity to 0, keeping one entry per food. Only an explicit statement counts.
- **Remove** ("删掉" / "扔了" / "坏了"): delete the entry. Nothing else is recorded.
- **View:** list by zone with expiry state; put eaten-up items on one short line ("已吃完：苹果、黄瓜").
- **Expiry state** is computed every time from `expires` and today's date, never stored: 已过期 = before today; 即将过期 = today through N days ahead (default 3). Ignore any `status` field in older files.
- **Expired items** stay in the file and out of meal suggestions. When showing them, ask once: "吃完了、扔了，还是还在？" — eaten: quantity 0; thrown away: remove; still fine: keep (change `expires` only if the user gives a date). No answer: change nothing.
- **No staples yet:** if the pantry has no long-cycle staples (grains, oils, dried goods, nuts) and `meta.longCycleProbed` is not true, ask once, briefly and warmly, whether they keep such staples. Record what they confirm in the ambient zone and set the flag once they answer. Never ask for a full inventory.

### Shopping list — shopping.json

- **Add / remove:** change only the requested entry (match unchecked entries by `itemKey`).
- **Bought** ("买了苹果"): mark the matching unchecked entry `checked: true` (keep it unchecked if they bought only part), update the pantry with the amount if known, and record the purchase.

### Purchases — history/YYYY-MM.json

- **Record:** one record per purchase. A current purchase uses today's date. For a past purchase with an unknown date, ask before recording; a past purchase alone does not change current stock or the list.
- **Stats:** after every write, recompute `stats.recordCount` and `stats.totalSpent` (known totals only, `null` when no total is known — say so when some are missing).
- **View / monthly stats:** read the month's file.

### Photos

- **Receipt or order screenshot:** a purchase report — handle it like "买了" for every item on it: the items are now at home and matching list entries are checked off, unless the user says otherwise. Record history with the printed date, quantities, prices and store. Name items by their everyday name (`伊利纯牛奶250ml×12` → 牛奶). Then list what you recorded so the user can correct it.
- **Photo of groceries, the fridge or a cupboard:** what you recognize is your guess, not the user's statement — even when they ask you to update from the photo. List the items (mark amounts as estimates), ask the user to confirm, and write only what they confirm. Never remove an item or set it to 0 because it is not visible.
- Leave out anything you cannot read clearly; ask if it matters.

### Preferences — profile.json

- Record explicit statements as they come up ("我不吃精制碳水" → `preferences.avoid`). Never run a questionnaire. Your guesses are not preferences until the user confirms them.
- Signature dishes the user confirms go to `exemplars`; workflow rules ("生成采购计划前先确认人数") go to `rules` and are followed in later plans.
- Feedback on a plan ("太油了") fixes the current output; save it only when the user means it to last.
- No profile is needed to plan. Create or update profile.json only when there is something to record. The first time it has content, show a short summary after the plan and set `confirmed: true` when the user confirms it.

## Planning

Read [planning.md](references/planning.md) before any of these:

| Request | Feature |
|---------|---------|
| "列个采购清单" / "这周买什么" | 🛒 Shopping plan — stock-aware list with quantities, written only after confirmation |
| "今晚吃什么" / "明天怎么搭" | 🍽 Meal pairings — from what is at home (plus the list for later days) |
| "海带怎么吃" in light of their stock or profile | 🥗 Ingredient advice — read-only |

## Scheduled Reminders (Optional)

If the host agent can run scheduled or periodic tasks, offer these reminders and create them with the host's own scheduling mechanism, in the user's local timezone, only after the user agrees. If the host has no such mechanism, skip this section; every check can also run on request (e.g. "看看有什么快过期").

Each reminder only reads data and sends a message in the user's language — it never modifies files. Any update happens later, from the user's reply, through the operations above.

| Reminder | Suggested schedule | Check | Message |
|----------|--------------------|-------|---------|
| Shopping list | Daily 12:00 and 17:30 | Read `[AGENT_HOME]/pantry/data/shopping.json`; count unchecked items | Only if count > 0: 🛒 Shopping List Reminder: You have {count} items to purchase |
| Expiring soon | Daily 08:00 | Read `[AGENT_HOME]/pantry/data/pantry.json`; items whose `expires` is within 3 days | ⚠️ {count} item(s) expiring soon: {item names} |
| Expired items | Daily or periodic | Same file; items past `expires` | ⚠️ {item names} 已过期——吃完了、扔了，还是还在？ |
| Low stock (optional) | Weekly, Monday 09:00 | Same file; items at quantity 0 or running low | Suggest adding them to the shopping list; add only after the user agrees |

## Formats

- IDs: `{type}_{6 random chars}` — `item_a1b2c3`, `shop_x9y8z7`, `rec_m5n6p7`, `ex_a1b2c3`
- Dates `YYYY-MM-DD`; datetimes ISO 8601 with timezone (`2026-04-01T17:45:00+08:00`)

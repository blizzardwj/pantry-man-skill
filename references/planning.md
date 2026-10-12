# Planning — shopping plan, meal pairings, ingredient advice

Read together with [SKILL.md](../SKILL.md); its ground rules still apply. Every plan starts from fresh reads of `profile.json` (if it exists), `pantry.json` and `shopping.json`. Follow the profile's `rules`; its health constraints override everything else here.

## 🛒 Shopping plan

Trigger: "列个采购清单" / "这周买什么" / "帮我看看买什么".

1. **Days covered:** the days the user names; otherwise one shopping trip starting today (or the shopping day they mention), lasting `profile.shoppingRhythm.daysPerTrip` (default 3–4 days). "这周买什么" plans the next trip only — the next one is planned when the user asks again, so it reflects what was actually bought and eaten.
2. **Start from what is there:**
   - Long-cycle staples (grains, oils, nuts, dried goods) already at home: skip, and say so briefly ("橄榄油已有，未列入").
   - Fresh food: subtract known stock from the need; unknown amount is not zero.
   - Unchecked list entries are already planned — don't add them again.
   - Eaten-up items (quantity 0) are candidates: include the ones that suit this plan, labelled "上次吃完，可补".
   - A confirmed signature dish (`profile.exemplars`) missing an ingredient: include it ("你的拿手菜『蒸鲷鱼山药』还差山药").
3. **Choose items** by category — 蔬菜 / 水果 / 蛋白质 / 油脂 / 主食 — with variety and a rough quantity each, following the profile's prefer / avoid. When fiber matters to the profile, prefer higher-fiber options (fiber table in [ingredient_knowledge.md](ingredient_knowledge.md); fresh and dry values are not comparable).
4. **Quantity check** with [quantity_benchmark.md](quantity_benchmark.md): assign items to its categories (蛋白质 splits into 鱼禽肉蛋 / 豆制品, 主食 into 谷类主食 / 薯类; oils and nuts are not checked). Target = daily range × days × `household.persons` (default 1). Show ✅ / ⚠️ / ❌ per category with a suggested amount — strict for fresh food, lenient for shelf-stable. Advisory only.
5. **Confirm, then write.** Show the list with the check; the user edits freely. Only after they confirm, add the confirmed items to `shopping.json` without duplicates and say "已加入购物清单" — this is not a purchase. Until then the proposal lives only in the conversation and is not available to meal pairings. Then offer meal pairings for the covered days.

## 🍽 Meal pairings

Trigger: "今晚吃什么" / "明天怎么搭" / "这几天怎么吃".

**Ingredient pool:**

- **Meals today** (or timing unclear): usable stock only — pantry items not at quantity 0 and not expired; unknown quantity counts as available.
- **Later days, or "买完之后":** usable stock plus unchecked shopping-list entries; mark each list item `（待买）` and spread them over the days so they get used.
- Nothing else: no eaten-up items, no unconfirmed proposals, nothing that is neither at home nor on the list.
- Today with an empty list: still answer from stock. If stock is too thin, say what is missing and offer a shopping plan.

**Each pairing has three parts:**

1. **食材** — ingredient names only, no dish names or cooking words ("冬瓜", not "冬瓜汤").
2. **价值** — one short nutritional reason for this combination.
3. **做法** — as few methods as possible for the whole combination. First try one method for everything (同锅煮 / 一起蒸 / 焯水拌油); split into groups only when needed (能生吃的不焯水), one sentence per group.

**Using the profile:** honor prefer / avoid and cookingStyle. When a confirmed signature dish fits the pool and the meal, reuse it ("照你上次的蒸鲷鱼山药做"), rotating when several fit.

**Output:** for today, only the requested meal(s). For later days, one block per day with 早 / 午 / 晚 as list items — shape only, generate your own content:

```
📅 周三（8/5）
- 早餐：<食材>（价值：…）→ 做法：…
```

Change only the meal the user asks to change.

## 🥗 Ingredient advice

Trigger: how to eat, season or pair a specific food or food category.

1. Find its category in [ingredient_knowledge.md](ingredient_knowledge.md). For fiber questions, also read the cross-category fiber table and check its 口径 (fresh / dry, insoluble / total) first.
2. Personalize with profile.json if it exists (e.g. 控钠 for liver concerns, no sugar when refined carbs are avoided); never create it here.
3. Answer with ① 特性 ② 提味／做法方向 ③ 安全建议. No fixed recipes; "今晚怎么吃这个" goes to meal pairings.

# pantry-man-skill 🧺

Plan what to buy and what to cook from what you already have at home. Your AI agent keeps track of your pantry, shopping list and purchases as you talk — or send a photo — so plans are based on your real stock, your diet and your shopping rhythm.

根据家里现有的食材，规划买什么、怎么吃。

## Features

**Plan from what you have**

- 🛒 **Shopping Plan** - A list for your next shopping trip that skips what you already have, suggests restocking foods you finished, and checks quantities against dietary guidelines. Nothing is added to your list until you confirm.
- 🍽 **Daily Pairings** - "What's for dinner?" answered from what is at home right now; plans for later days can also use your shopping list.
- 🥗 **Ingredient Advice** - How to cook, season and pair a food, adjusted to your dietary profile.

**Kept up to date as you go**

- 📦 **Pantry** - What you have, by storage zone (fridge / freezer / ambient / daily items). Finished foods stay at zero as a restock hint.
- ⏰ **Expiry Tracking** - Expiring items are flagged; expired items stay listed until you say they were eaten, thrown away, or are still fine.
- 🧾 **Shopping List & Purchase History** - Mark items bought, keep monthly purchase records and spending.
- 🔄 **Learns as you go** - Remembers the preferences, signature dishes and rules you state. No questionnaire.

## Installation

```bash
npx skills add blizzardwj/pantry-man-skill
```

## Usage

Once installed, just talk to your agent — in Chinese or English; it replies in your language and keeps item names as you say them:

**Planning**

- "列个采购清单" / "这周买什么" — a shopping plan for your next trip, then meal pairings for those days
- "今晚吃什么" / "What should I cook tonight?" — a meal from what you already have
- "我在控糖，海带怎么吃比较好" — ingredient advice adjusted to your profile

**Keeping track**

- "买了两盒牛奶" / "I bought 2L of milk" — stocks the pantry, checks it off the list, records the purchase
- "苹果吃完了" / "I finished the apples" — keeps apples at zero so the next shopping plan can suggest them
- "冰箱里有什么" / "What's expiring this week?" — your stock with expiry flags
- "以后早餐多安排苹果" — remembers a preference for future plans
- "Show my purchase history for last month"

### Say it or show it (voice and photos)

With a voice-enabled host you can report several changes in one sentence, right at the store or the fridge:

> "买了两盒牛奶和一把菠菜，鸡蛋吃完了，过期的酸奶扔了"

The agent applies each part separately — milk and spinach go into the fridge and milk is checked off the shopping list, eggs stay at zero as a restock hint, the yogurt is removed — and replies with a short summary of what changed.

You can also send a photo:

- **Receipt or order screenshot** — recorded as a purchase right away: items go into the pantry, matching list entries are checked off, and the printed prices, date and store go into your purchase history. The agent then shows what it recorded so you can correct it.
- **Groceries, fridge or cupboard** — the agent lists what it recognizes (amounts as estimates) and updates the pantry only after you confirm. Items not visible in the photo are never treated as gone.

## Data Structure

All data is stored in JSON files under `[AGENT_HOME]/pantry/data/`:

| File | Purpose |
|------|---------|
| `pantry.json` | Food inventory by zone |
| `shopping.json` | Shopping list |
| `history/YYYY-MM.json` | Monthly purchase records |
| `profile.json` | Dietary profile (preferences, household, shopping rhythm, signature dishes) |

See [references/schema.md](references/schema.md) for complete schema definitions.

## Recommended Hosts

Pantry updates happen in the kitchen and at the store, not at a desk. The skill works best in a **personal-assistant agent such as Hermes** — one that:

- **accepts voice input and photos**, so one sentence or one picture can carry several updates;
- **is reachable from your phone or a chat app**, so you can say "买了…" right after shopping;
- **keeps running and can schedule tasks**, so the optional reminders (shopping list, expiring items) arrive on time.

Any agent that supports the Open Agent Skills specification can run it, including coding agents such as Claude Code, Cursor, Cline and Codex. Those are handy for trying the skill out and for development and testing (see `dev/`), but less convenient for day-to-day kitchen use.

## License

MIT License - feel free to use and modify!

## Contributing

Issues and pull requests are welcome!

---

Made with ❤️ for smarter kitchens

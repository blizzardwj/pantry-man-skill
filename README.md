# pantry-man-skill 🧺

A skill for AI agents to manage home pantry inventory, shopping lists, and purchase history.

## Features

- 📦 **Inventory Management** - Track food items by storage zone (cold/frozen/ambient/daily)
- 🛒 **Shopping List** - Manage shopping items with priorities and categories
- 📊 **Purchase History** - Record and view purchase history with monthly stats
- ⏰ **Expiry Tracking** - Check items expiring soon; expired items stay listed until you say they were eaten, thrown away, or are still fine
- 🔄 **Learns as you go** - Remembers the preferences and signature dishes you state. Foods you report eating up stay in the pantry at zero and may be suggested in the next shopping plan; restocking clears them.
- 🗓️ **Meal Planning** - 🛒 Shopping Plan (stock-aware list for your next shopping trip, with a dietary-guideline quantity check, written only after you confirm), 🍽 Daily Pairings (meals for today from current stock; plans for later days can also use your shopping list), and 🥗 Ingredient Advice — all driven by a lightweight dietary profile

## Installation

```bash
npx skills add blizzardwj/pantry-man-skill
```

## Usage

Once installed, your AI agent can help you with:

- "Show me what's in my refrigerator"
- "Add 2L milk to my pantry, expires in 7 days"
- "Add tomatoes to my shopping list"
- "苹果买了" (updates inventory and purchase history, and marks apples on the shopping list as bought)
- "Record a purchase: milk 15 yuan, bread 12 yuan"
- "What items are expiring this week?"
- "Show my purchase history for last month"
- "苹果吃完了" (keeps apples in the pantry at zero so the next shopping plan can suggest them)
- "以后早餐多安排苹果" (records a stated preference for future pairings)
- "列个采购清单" (Shopping Plan — stock-aware list with quantity check + confirmation step)
- "今晚吃什么" (Daily Pairings — tonight's meal from what you already have; plans for later days can also use your confirmed shopping list)
- "这周买什么" (Shopping Plan for your next trip, then meal pairings for those days)

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

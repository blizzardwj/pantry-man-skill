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

## Data Structure

All data is stored in JSON files under `[AGENT_HOME]/pantry/data/`:

| File | Purpose |
|------|---------|
| `pantry.json` | Food inventory by zone |
| `shopping.json` | Shopping list |
| `history/YYYY-MM.json` | Monthly purchase records |
| `profile.json` | Dietary profile (preferences, household, shopping rhythm, signature dishes) |

See [references/schema.md](references/schema.md) for complete schema definitions.

## Compatibility

Works with AI agents that support the Open Agent Skills specification:

- Claude Code
- Cursor
- Cline
- Codex
- And more...

## License

MIT License - feel free to use and modify!

## Contributing

Issues and pull requests are welcome!

---

Made with ❤️ for smarter kitchens

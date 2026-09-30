# pantry-man-skill 🧺

A skill for AI agents to manage home pantry inventory, shopping lists, and purchase history.

## Features

- 📦 **Inventory Management** - Track food items by storage zone (cold/frozen/ambient/daily)
- 🛒 **Shopping List** - Manage shopping items with priorities and categories
- 📊 **Purchase History** - Record and view purchase history with monthly stats
- ⏰ **Expiry Tracking** - Check items expiring soon
- 🔄 **Feedback Loop** - Learns from stated preferences, feedback on meal plans, and foods you report eating until they are gone. Ordinary purchases and stock edits update inventory and purchase history without becoming preference feedback. Depleted foods may be suggested again; replenishing them clears that signal.
- 🗓️ **Meal Planning** - Three modes: 🛒 Shopping Plan (stock-aware shopping list with a dietary-guideline quantity check and a confirmation step), 🍽 Daily Pairings (per-day breakfast/lunch/dinner combos drawn from your confirmed list + stock), and 📆 Weekly Plan (chains both per your shopping rhythm, segment by segment) — all driven by a lightweight dietary profile

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
- "苹果吃完了" (updates inventory and keeps a possible replenishment signal for later plans)
- "以后早餐多安排苹果" (records a stated preference for future pairings)
- "列个采购清单" (Shopping Plan — stock-aware list with quantity check + confirmation step)
- "今晚吃什么" (Daily Pairings — per-day meal combos from your list + stock)
- "这周买什么" (Weekly Plan — chains both, segment by segment)

## Data Structure

All data is stored in JSON files under `pantry/data/`:

| File | Purpose |
|------|---------|
| `pantry.json` | Food inventory by zone |
| `shopping.json` | Shopping list |
| `history/YYYY-MM.json` | Monthly purchase records |
| `feedback.json` | Personalization signals, including consumed foods and stated preferences |
| `profile.json` | Dietary profile (preferences, household, shopping rhythm) |
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

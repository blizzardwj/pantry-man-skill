# pantry-man-skill 🧺

A skill for AI agents to manage home pantry inventory, shopping lists, and purchase history.

## Features

- 📦 **Inventory Management** - Track food items by storage zone (cold/frozen/ambient/daily)
- 🛒 **Shopping List** - Manage shopping items with priorities and categories
- 📊 **Purchase History** - Record and view purchase history with monthly stats
- ⏰ **Expiry Tracking** - Check items expiring soon
- 🔄 **Feedback Loop** - Captures corrections, new facts, and stock changes from conversation into `feedback.json`; reflects them into profile preferences, pairing templates, user-level rules, and inventory (three-layer triggers, depleted-candidate refills)
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
- "Record a purchase: milk 15 yuan, bread 12 yuan"
- "What items are expiring this week?"
- "Show my purchase history for last month"
- "我今天的早餐是鸡肉、南瓜、青椒、自制酸奶" (Feedback Loop — the agent records new facts and refines future plans)
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
| `feedback.json` | User feedback log (drives profile/template/rule refinement) |
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

# pantry-man-skill 🧺

A skill for AI agents to manage home pantry inventory, shopping lists, and purchase history.

## Features

- 📦 **Inventory Management** - Track food items by storage zone (cold/frozen/dry)
- 🛒 **Shopping List** - Manage shopping items with priorities and categories
- 📊 **Purchase History** - Record and view purchase history with monthly stats
- ⏰ **Expiry Tracking** - Check items expiring soon

## Installation

```bash
npx skills add your-username/pantry-man-skill
```

## Usage

Once installed, your AI agent can help you with:

- "Show me what's in my refrigerator"
- "Add 2L milk to my pantry, expires in 7 days"
- "Add tomatoes to my shopping list"
- "Record a purchase: milk 15 yuan, bread 12 yuan"
- "What items are expiring this week?"
- "Show my purchase history for last month"

## Data Structure

All data is stored in JSON files under `pantry/data/`:

| File | Purpose |
|------|---------|
| `pantry.json` | Food inventory by zone |
| `shopping.json` | Shopping list |
| `history/YYYY-MM.json` | Monthly purchase records |

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

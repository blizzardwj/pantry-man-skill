---
name: pantry-man
description: Manage home pantry inventory, shopping lists, and purchase history. Use when the user asks about (1) adding/viewing/searching inventory by zone (cold/frozen/ambient/daily), (2) managing shopping lists for food and daily items, (3) recording purchases and viewing purchase history, (4) checking expiry dates or items running low.
---

# Pantry Management

Manage home inventory, shopping lists, and purchase records.

## Data Location

All data files are under `pantry/data/`:

| File | Purpose |
|------|---------|
| `pantry.json` | Inventory (cold/frozen/ambient/daily zones) |
| `shopping.json` | Shopping list (food/daily categories) |
| `history/YYYY-MM.json` | Purchase records by month |

## Core Operations

### Inventory

**View by zone:**
```
Read pantry.json → Format items from zones.cold/frozen/ambient/daily
```

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
```

**View history:**
```
Read history/YYYY-MM.json → Format records
```

**Monthly stats:**
```
Read history/YYYY-MM.json → Return stats.totalSpent and stats.recordCount
```

## Item ID Generation

Use format: `{type}_{random_6_chars}` (e.g., `item_a1b2c3`, `shop_x9y8z7`, `rec_m5n6p7`)

## Timestamp Format

- Dates: `YYYY-MM-DD` (e.g., `2026-04-01`)
- Datetimes: ISO 8601 with timezone (e.g., `2026-04-01T17:45:00+08:00`)

## References

- See [schema.md](references/schema.md) for complete data structure definitions.

## Heartbeat Integration (Optional)

Add these tasks to your `HEARTBEAT.md` for periodic reminders:

### Shopping List Reminder

Check pending shopping items and remind user:

```
1. Read pantry/data/shopping.json
2. Count unchecked items in categories.food.items and categories.daily.items
3. If count > 0, remind: "You have {count} items on your shopping list"
```

### Expiry Alert

Check items expiring soon:

```
1. Read pantry/data/pantry.json
2. For each zone, filter items where expires date is within 3 days
3. If found, alert: "{count} items are expiring soon: {item names}"
```

### Low Stock Alert (Optional)

Define minimum stock thresholds and check:

```
1. Read pantry/data/pantry.json
2. Check if essential items are running low or missing
3. Suggest adding to shopping list if needed
```

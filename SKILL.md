---
name: pantry-man
description: Manage home pantry inventory, shopping lists, and purchase history. Use when the user asks about (1) adding/viewing/searching inventory by zone (cold/frozen/ambient/daily), (2) managing shopping lists for food and daily items, (3) recording purchases and viewing purchase history, (4) checking expiry dates or items running low.
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

## Scheduled Reminders (Recommended)

Use cron jobs for time-specific reminders. These align with user's daily routine.

### Shopping List Reminder

Remind user to check shopping list during lunch break and after work:

```bash
# Add cron jobs (Asia/Shanghai timezone)
cron add "0 12 * * *" "Check pantry/data/shopping.json for unchecked items. If count > 0, remind: 🛒 购物提醒：你有 {count} 件商品待购买"
cron add "30 17 * * *" "Check pantry/data/shopping.json for unchecked items. If count > 0, remind: 🛒 购物提醒：你有 {count} 件商品待购买"
```

### Expiry Alert

Remind user in the morning about items expiring soon:

```bash
cron add "0 8 * * *" "Check pantry/data/pantry.json for items expiring within 3 days. If found, alert: ⚠️ {count} 件商品即将过期: {item names}"
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
